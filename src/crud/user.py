from enum import Enum
from secrets import token_urlsafe

from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

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
        SELECT
            parent_child.parent_id,
            parent_child.child_id
        FROM parent_child
        JOIN {user_type}
        USING ({user_id})
        
        """


crud_user = CRUDUser(model=ParentChild)
