from enum import Enum
from secrets import token_urlsafe

from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

from src.core import get_settings
from src.crud.base import CRUDBase
from src.model import ParentChild
from src.schema import CreateUser
from src.util import get_current_datetime, convert_datetime_to_string


class CRUDUser(CRUDBase):
    def sign_in(self, db: Session, user_data: CreateUser) -> str:
        query: str = f"""
        WITH RECURSIVE user (id, type, account, password, nickname) AS (
            SELECT id, type, account, password, nickname
            FROM parent
            WHERE account = '{user_data.account}'
            UNION ALL
            SELECT id, type, account, password, nickname
            FROM child
            WHERE account = '{user_data.account}'
        )
        
        SELECT *
        FROM user;
        """
        result = db.execute(statement=query).fetchone()
        if result:
            password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if password_ctx.verify(
                secret=user_data.password, hash=result["password"]
            ):
                if result["type"] == "MOTHER" or result["type"] == "FATHER":
                    user_type: str = "parent"
                else:
                    user_type: str = "child"
                    
                encoded_data: dict = {
                    "user_id": result["id"],
                    "user_type": user_type,
                    "user_account": result["account"],
                    "user_nickname": result["nickname"],
                    "detailed_type": result["type"]
                }
                access_token = jwt.encode(
                    claims=encoded_data,
                    key=get_settings().SECRET_KEY,
                    algorithm=get_settings().ALGORITHM
                )
                
                return access_token

            else:
                return None
                    
        else:
            return None
        
    
    def sign_up(self, token: str, db: Session, insert_data: CreateUser) -> bool:
        password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        converted_insert_data = insert_data.dict(exclude_none=True)
        converted_insert_data["password"] = password_ctx.hash(
            secret=converted_insert_data["password"]
        )
        
        user_type: str = converted_insert_data.pop("user_type")
        columns: str = ",".join(
            [ column for column in converted_insert_data.keys() ]
        )
        
        values: str = ""
        for value in converted_insert_data.values():
            if isinstance(value, str):
                values += f"\'{value}\',"
            elif isinstance(value, Enum):
                values += f"\'{value.name}',"
            else:
                values += f"{value},"
                
        current_datetime = convert_datetime_to_string(get_current_datetime())
        values += f"\'{current_datetime}\',\'{current_datetime}\'"
        
        if user_type == "parent":
            create_parent_query: str = f"""
            INSERT INTO parent (
                {columns},
                created_at,
                nickname_updated_at
            )
            VALUES ({values});
            """
            db.execute(statement=create_parent_query)
            db.commit()
        
        else:
            values += f",\'{current_datetime}\'"
            create_child_query: str = f"""
            INSERT INTO child (
                {columns},
                created_at,
                nickname_updated_at,
                character_name_updated_at
            )
            VALUES ({values});
            """
            db.execute(statement=create_child_query)
            db.commit()
            
            create_parent_child_query: str = f"""
            INSERT INTO parent_child
            (parent_id, child_id, level_id, created_at, experience)
            VALUES (
                (SELECT id FROM parent WHERE invitation_code = '{token}'),
                (SELECT id FROM child WHERE account = '{
                    converted_insert_data["account"]
                }'),
                (SELECT id FROM level WHERE required_experience = 'LEVEL_1'),
                '{current_datetime}',
                0
            );
            """
            db.execute(statement=create_parent_child_query)
            db.commit()
            
            create_diary_query: str = f"""            
            INSERT INTO question_diary
            (child_id, question_id, created_at)
            VALUES (
                (SELECT id FROM child WHERE account = '{
                    converted_insert_data["account"]
                }'),
                (SELECT id FROM question ORDER BY RAND() LIMIT 1),
                '{current_datetime}'
            )
            """
            db.execute(statement=create_diary_query)
            db.commit()            
            
        
        return True


    def invite(self, db: Session, user_id: int) -> str:
        invitation_code: str = token_urlsafe(6)
        current_datetime = convert_datetime_to_string(get_current_datetime())
        query: str = f"""
        UPDATE parent
        SET invitation_code = '{invitation_code}', invitation_code_expired_date = '{current_datetime}'
        WHERE id = {user_id};
        """
        db.execute(statement=query)
        db.commit()
        
        return invitation_code
    
    
    def get_activity_likes(
        self, db: Session, user_id: int, user_type: str
    ) -> list[dict]:
        query: str = f"""
        WITH RECURSIVE user (id, type) AS (
            SELECT parent_id AS id, "parent" AS type
            FROM parent_child
            WHERE {user_type}_id = {user_id}
            UNION
            SELECT child_id AS id, "child" AS type
            FROM parent_child
            WHERE {user_type}_id = {user_id}
        ), Likes (user_type, activity_id) AS (
            SELECT
                user.type AS user_type,
                parent_activity_like.activity_id AS activity_id
            FROM user
            JOIN parent_activity_like
            ON (
                parent_activity_like.is_visited = 0
                AND
                user.id = parent_activity_like.parent_id
            )
            UNION
            SELECT
                user.type AS user_type,
                child_activity_like.activity_id AS activity_id
            FROM user
            JOIN child_activity_like
            ON (
                child_activity_like.is_visited = 0
                AND
                user.id = child_activity_like.child_id
            )
        )

        SELECT 
            users,
            activity.*
        FROM (
            SELECT
                activity_id AS id,
                GROUP_CONCAT(user_type) AS users
            FROM Likes
            GROUP BY id         
        ) AS UserLikes
        JOIN activity
        USING (id);
        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        converted_result: list[dict] = jsonable_encoder(result)
        
        for data in converted_result:
            data["users"] = data["users"].split(",")
        
        return converted_result
    

    def visit_activity(
        self, db: Session, user_id: int, user_type: str, activity_id: int
    ) -> bool:
        query: str = f"""
        UPDATE {user_type}_activity_like
        SET is_visited = 1
        WHERE (
            activity_id = {activity_id}
            AND
            {user_type}_id = {user_id}
        );
        """
        db.execute(statement=query)
        db.commit()
        
        return True


    def get_latest_diary(
        self, db: Session, user_id: int, user_type: str
    ) -> dict:
        if user_type == "parent":
            select_child_query: str = f"""
            SELECT child_id
            FROM parent_child
            WHERE parent_child.parent_id = {user_id}
            """
            child_result = db.execute(statement=select_child_query).fetchone()
            db.commit()
            
            child_id: int = child_result["child_id"]
        
        else:
            child_id: int = user_id
            
        select_question_diary_query: str = f"""
        SELECT
            child.nickname,
            diary.id,
            level.id AS level_id,
            parent_child.experience AS current_experience,
            level.required_experience AS required_experience,
            diary.question_content,
            CASE
                WHEN diary.content IS NULL THEN level.ordinary_character_image_url
                WHEN question_diary_reply.answered_at IS NULL THEN level.child_to_parent_character_image_url
                ELSE level.parent_to_child_character_image_url
            END AS character_image_url,
            IF(diary.content IS NULL, 0 ,1) AS is_child_answered,
            IF(question_diary_reply.answered_at IS NULL, 0, 1) AS is_parent_answered
        FROM (
            SELECT
                specific_child.id,
                specific_child.child_id,
                specific_child.emotion_id,
                specific_child.content,
                question.id AS question_id,
                question.content AS question_content
            FROM (
                SELECT *
                FROM question_diary
                WHERE child_id = {child_id}
            ) AS specific_child
            JOIN question
            ON specific_child.question_id = question.id
            ORDER BY answered_at IS NULL, answered_at DESC
            LIMIT 1
        ) AS diary
        JOIN child
        ON diary.child_id = child.id
        JOIN parent_child
        ON diary.child_id = parent_child.child_id
        JOIN level
        ON parent_child.level_id = level.id
        LEFT JOIN question_diary_reply
        ON diary.id = question_diary_reply.question_diary_id 
        """
        question_diary_result = db.execute(
            statement=select_question_diary_query
        ).fetchone()
        db.commit()
        
        return jsonable_encoder(question_diary_result)
    
    
    def get_diaries(
        self, db: Session, user_id: int, user_type: str
    ) -> dict:        
        query: str = f"""
        WITH activity_diaries (
            is_child_answered
        ) AS (
            SELECT
                IF(activity_diary.answered IS NULL 0, 1) is_child_answered
            FROM (
                SELECT 
                FROM child_ativity_like
                WHERE child_id = (
                    SELECT child_id
                    FROM parent_child
                    WHERE {user_type}_id = {user_id}
                )
            ) AS child_liked_activity
            JOIN activity_diary
            ON child_liked_activity.id = activity_diary.child_activity_like_id    
            JOIN activity_diary_reply
            ON activity_diary.id = activity_diary_reply.activity_diary_id
        ), question_diaries (
            id,
            type,
            emotion_type,
            answered_at,
            is_child_answered,
            is_parent_answered
        ) AS (
            SELECT
                child_diary.question_diary_id AS id,            
                "quesiton" AS type,
                emotion.type AS emotion_type,
                child_diary.answered_at AS answered_at,
                IF(child_diary.answered_at IS NULL, 0, 1) AS is_child_answered,
                IF(question_diary_reply.answered_at IS NULL, 0, 1) AS is_parent_answered
            FROM (
                SELECT
                    id AS question_diary_id,
                    emotion_id,
                    answered_at
                FROM question_diary
                WHERE child_id = (
                    SELECT child_id
                    FROM parent_child
                    WHERE {user_type}_id = {user_id}
                )
            ) AS child_diary
            JOIN question_diary_reply
            USING(question_diary_id)
            JOIN emotion
            ON child_diary.emotion_id = emtion.id
        )
        
        SELECRT *
        FROM question_diaries
        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        return converted_result
            
    
    def write_diary(self, db: Session) -> dict:
        pass
        
        
    def get_family_information(self, db: Session) -> dict:
        """
        
        """
        

crud_user = CRUDUser(model=ParentChild)
