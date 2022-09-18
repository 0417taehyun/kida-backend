from enum import Enum
from datetime import timedelta
from secrets import token_urlsafe

from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

from src.core import get_settings
from src.crud.base import CRUDBase
from src.model import ParentChild, LevelType
from src.schema import CreateUser, CreateDiary, CreateDiaryReply
from src.util import get_current_datetime, convert_datetime_to_string


class CRUDUser(CRUDBase):
    def sign_in(self, db: Session, user_data: CreateUser) -> str:
        query: str = f"""
        WITH RECURSIVE user (
            id, type, account, password, nickname
        ) AS (
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
                
                return {"token": access_token}

            else:
                return None
                    
        else:
            return None
        
    
    def sign_up(self, invitation_code: str, db: Session, insert_data: CreateUser) -> bool:
        password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        converted_insert_data = insert_data.dict(exclude_none=True)
        converted_insert_data["password"] = password_ctx.hash(
            secret=converted_insert_data["password"]
        )
        
        user_type: str = converted_insert_data.pop("user_type")                
        
        
        if invitation_code:
            if user_type == "parent":
                invite_table = "child"
                invited_table = "parent"
            
            else:
                invite_table = "parent"
                invited_table = "child"
            
            select_invitation_code_query: str = f"""
            SELECT invitation_code_expired_date
            FROM {invite_table}
            WHERE  invitation_code = '{invitation_code}';
            """
            
            invitation_code_result = db.execute(
                statement=select_invitation_code_query
            ).fetchone()
            db.commit()
            
            if not invitation_code_result:
                raise ValueError("invalid invitation code")
            
            elif(
                (invitation_code_result[
                    "invitation_code_expired_date"
                ]
                ).timestamp()
                <
                (
                    get_current_datetime()
                    -
                    timedelta(
                        hours=get_settings().INVITATION_CODE_EXPIRED_HOURS
                    )
                ).timestamp()
            ):
                raise ValueError("invitation code expired")
                        
            else:
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
                    
                    create_diary_query: str = f"""
                    INSERT INTO diary (type, created_at)
                    VALUES ('question', '{current_datetime}');
                    """
                    db.execute(statement=create_diary_query)
                    db.commit()
                    
                    create_question_diary_query: str = f"""            
                    INSERT INTO question_diary
                    (child_id, question_id, diary_id, created_at)
                    VALUES (
                        (SELECT id FROM child WHERE account = '{
                            converted_insert_data["account"]
                        }'),
                        (SELECT id FROM question ORDER BY RAND() LIMIT 1),
                        (
                            SELECT id
                            FROM diary
                            WHERE type = 'question'
                            ORDER BY id DESC
                            LIMIT 1
                        ),
                        '{current_datetime}'
                    )
                    """
                    db.execute(statement=create_question_diary_query)
                    db.commit()              
                
                create_parent_child_query: str = f"""
                INSERT INTO parent_child
                (
                    {invite_table}_id,
                    {invited_table}_id,
                    created_at,
                    invitation_code
                )
                VALUES (
                    (SELECT id FROM {invite_table} WHERE invitation_code = '{invitation_code}'),
                    (SELECT id FROM {invited_table} WHERE account = '{
                        converted_insert_data["account"]
                    }'),
                    '{current_datetime}',
                    '{invitation_code}'
                );
                """
                db.execute(statement=create_parent_child_query)
                db.commit()
                
                
                update_invitation_code_query: str = f"""
                UPDATE {invite_table}
                SET invitation_code = NULL, invitation_code_expired_date = NULL;
                """
                db.execute(statement=update_invitation_code_query)
                db.commit()
                        
                return True
            
        else:
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
                
                create_diary_query: str = f"""
                INSERT INTO diary (type, created_at)
                VALUES ('question', '{current_datetime}');
                """
                db.execute(statement=create_diary_query)
                db.commit()
                
                create_question_diary_query: str = f"""            
                INSERT INTO question_diary
                (child_id, question_id, diary_id, created_at)
                VALUES (
                    (SELECT id FROM child WHERE account = '{
                        converted_insert_data["account"]
                    }'),
                    (SELECT id FROM question ORDER BY RAND() LIMIT 1),
                    (
                        SELECT id
                        FROM diary
                        WHERE type = 'question'
                        ORDER BY id DESC
                        LIMIT 1
                    ),
                    '{current_datetime}'
                )
                """
                db.execute(statement=create_question_diary_query)
                db.commit()
                        
            return True


    def invite(self, db: Session, user_type: str, user_id: int) -> str:
        invitation_code: str = token_urlsafe(6)
        current_datetime = convert_datetime_to_string(get_current_datetime())
        query: str = f"""
        UPDATE {user_type}
        SET invitation_code = '{invitation_code}', invitation_code_expired_date = '{current_datetime}'
        WHERE id = {user_id};
        """
        db.execute(statement=query)
        db.commit()
        
        return {"invitation_code": invitation_code}
    
    
    def get_invitation_code(self, db: Session, user_id: int) -> dict:
        query: str = f"""
        SELECT invitation_code
        FROM parent
        WHERE id = {user_id};
        """
        result = db.execute(statement=query).fetchone()
        db.commit()
        
        return jsonable_encoder(result)
    
    
    def get_invited_users(
        self, db: Session, user_id: int, user_type: str
    ) -> dict:
        if user_type == "parent":
            invited_table: str = "child"
        else:
            invited_table: str = "parent"            
            
        query: str = f"""
        SELECT
            {invited_table}.id,
            {invited_table}.account,
            {invited_table}.created_at,
            parent_child.invitation_code,
            user.character_name        
        FROM (
            SELECT
                id AS {user_type}_id,
                invitation_code,
                IF(
                    STRCMP('{invited_table}', 'child') = 0,
                    character_name,
                    NULL
                ) AS character_name                
            FROM {user_type}
            WHERE id = {user_id}
        ) AS user
        LEFT JOIN parent_child
        USING ({user_type}_id)
        JOIN {invited_table}
        ON parent_child.{invited_table}_id = {invited_table}.id;        
        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        return jsonable_encoder(result)
    
    
    def check_if_user_sign_up_by_invitation_code(
        self, db: Session, invitation_code: str, user_type: str
    ) -> dict:
        if user_type == "parent":
            invited_table: str = "child"
        else:
            invited_table: str = "parent"            
            
        query: str = f"""
        SELECT
            {invited_table}.id,
            {invited_table}.account,
            {invited_table}.created_at,
            parent_child.invitation_code            
        FROM parent_child
        JOIN {invited_table}
        ON (
            parent_child.invitation_code = '{invitation_code}'
            AND 
            parent_child.{invited_table}_id = {invited_table}.id
        );
        """
        result = db.execute(statement=query).fetchone()
        db.commit()
        
        return jsonable_encoder(result)
    
    
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
        current_datetime = convert_datetime_to_string(get_current_datetime())
        
        
        update_visit_query: str = f"""
        UPDATE {user_type}_activity_like
        SET is_visited = 1
        WHERE (
            activity_id = {activity_id}
            AND
            {user_type}_id = {user_id}
        );
        """
        db.execute(statement=update_visit_query)
        db.commit()
        
        create_diary_query: str = f"""
        INSERT INTO diary (type, created_at)
        VALUES ('activity', '{current_datetime}')
        """
        db.execute(statement=create_diary_query)
        db.commit()
        
        create_activity_diary_query: str = f"""
        INSERT INTO activity_diary
        (child_activity_like_id, diary_id, created_at)
        VALUES (
            (
                SELECT id
                FROM {user_type}_activity_like
                WHERE (
                    activity_id = {activity_id}
                    AND
                    {user_type}_id = {user_id}
                    AND
                    is_visited = 1
                )
            ),
            (
                SELECT id
                FROM diary
                WHERE type = 'activity'
                ORDER BY id DESC LIMIT 1
            ),
            '{current_datetime}'
        );
        """
        db.execute(statement=create_activity_diary_query)
        db.commit()
        
        return True


    def get_diary(
        self, db: Session, diary_id: int, child_id: int, user_type: str
    ) -> dict:
        if diary_id:
            query: str = f"""
            WITH RECURISVE (
                SELECT
                
                FROM diary
                JOIN (
                    SELECT
                    
                    FROM question_diary
                    SELECT
                    
                    
                    SELECT id
                    FROM child
                    WHERE id = {child_id}
                )
                ON
                
            )
            """
        
        # else:
        #     query: str = f"""
        #     SELECT
        #         latest_diary.diary_id,
        #         latest_diary.child_id,
        #         latest_diary.answered_at,
        #         latest_diary.question_id,
        #         COUNT(question_diary_reply.parent_id) AS parent_answered_count
        #     FROM (
        #         SELECT
        #             diary_id,
        #             child_id,
        #             answered_at,
        #             question_id
        #         FROM question_diary
        #         WHERE child_id = {child_id}
        #         ORDER BY answered_at IS NULL, answered_at DESC
        #         LIMIT 1
        #     ) AS latest_diary
        #     LEFT JOIN question_diary_reply
        #     USING (diary_id)
        #     GROUP BY (
        #         latest_diary.diary_id,
        #         latest_diary.child_id,
        #         latest_diary.answered_at,
        #         latest_diary.question_id
        #     )          
        #     """
        #     result = db.execute(statement=query).fetchone()
        #     db.commit()
            
        #     converted_data: dict = jsonable_encoder(result)
        #     levels: dict = { enum.name: enum.value for enum in LevelType }
        #     converted_data["required_experience"] = levels[
        #         converted_data["required_experience"]
        #     ]
            
        #     return jsonable_encoder(converted_data)            

        
        else:
            if user_type == "parent":
                select_child_query: str = f"""
                SELECT child_id
                FROM parent_child
                WHERE parent_child.parent_id = {child_id};
                """
                child_result = db.execute(statement=select_child_query).fetchone()
                db.commit()
                
                child_id: int = child_result["child_id"]
                
            select_question_diary_query: str = f"""
            SELECT
                child.character_name,
                child.nickname,
                diary.id,
                level.id AS level_id,
                child.experience AS current_experience,
                level.required_experience,
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
                    specific_child.diary_id,
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
            JOIN level
            ON child.level_id = level.id
            LEFT JOIN question_diary_reply
            ON diary.diary_id = question_diary_reply.diary_id ;
            """
            question_diary_result = db.execute(
                statement=select_question_diary_query
            ).fetchone()
            db.commit()
            
            converted_data: dict = jsonable_encoder(question_diary_result)
            levels: dict = { enum.name: enum.value for enum in LevelType }
            converted_data["required_experience"] = levels[
                converted_data["required_experience"]
            ]
            
            return jsonable_encoder(converted_data)
    
    
    def get_diaries(self, db: Session, child_id: int) -> dict:
        query: str = f"""
        WITH RECURSIVE question_diaries (
            SELECT
            
            FROM (
                SELECT
                    question_diary.diary_id AS id,
                    question_diary_id AS question_diary_id
                FROM question_diary
                WHERE child_id = {child_id}
            )
            JOIN diary
            USING (id)
            LEFT JOIN question_diary_reply
            USING (question_diary_id)
        )
        
        SELECT *
        FROM question_diaries

        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        return jsonable_encoder(result)
            
    
    def write_diary(
        self,
        db: Session,
        user_id: int,
        user_type: str,
        diary_type: str,
        diary_id: int,
        insert_data: CreateDiary | CreateDiaryReply
    ) -> dict:
        table: str = f"{diary_type}_diary"            
        converted_insert_data: dict = insert_data.dict(exclude_none=True)  
        current_datetime = convert_datetime_to_string(get_current_datetime())            
        
        if user_type == "parent":
            table += "_reply"
            columns: str = ",".join(
                [ column for column in converted_insert_data.keys()]
            )
            
            values: str = ""
            for value in converted_insert_data.values():
                if isinstance(value, str):
                    values += f"\'{value}\',"
                else:
                    values += f"{value},"
            
            values += f"\'{current_datetime}\'"
                    
            query: str = f"""
            INSERT INTO {table}
            ({columns}, created_at, answered_at, {user_type}_id, diary_id)
            VALUES({values}, '{current_datetime}', {user_id}, {diary_id});
            """
            
        else:
            set_statement: str = ""
            for column, value in converted_insert_data.items():
                if isinstance(value, str):
                    set_statement += f"{column}=\'{value}\',"
                else:
                    set_statement += f"{column}={value},"

            set_statement += f"answered_at=\'{current_datetime}\'"              
            
            query: str = f"""
            UPDATE {table} SET {set_statement}
            WHERE diary_id = {diary_id};
            """
            
        db.execute(statement=query)
        db.commit()
    
        return True
        
       
    def get_family_information(self, db: Session) -> dict:
        query = f"""
        
        """
    
    def create_family_information(self, db: Session, insert_data) -> bool:
        query = f"""
        
        """
        

crud_user = CRUDUser(model=ParentChild)
