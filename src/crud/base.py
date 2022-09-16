from enum import Enum
from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from src.database import Base
from src.util import convert_datetime_to_string, get_current_datetime


Model = TypeVar("Model", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model]) -> None:
        self.model = model
    
    def get_one_by_id(self, db: Session, id: int):
        """
        
        """
        query: str = f"""
        SELECT *
        FROM {self.model.__tablename__}
        WHERE id = {id};
        """
        result = db.execute(statement=query).fetchone()
        return result
        
    
    def get_multi(self, db: Session):
        """
        
        """
        query: str = f"""
        SELECT *
        FROM {self.model.__tablename__}
        """
        result = db.execute(statement=query).fetchall()
        return jsonable_encoder(result)
    
    
    def create(self, db: Session, insert_data: CreateSchema) -> bool:
        """
        
        """
        converted_insert_data: dict = insert_data.dict(exclude_none=True)
        
        columns: str = ",".join(
            [ column for column in converted_insert_data.keys()]
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
        values += f"\'{current_datetime}\'"        
        
        query: str = f"""
        INSERT INTO {self.model.__tablename__}
        ({columns},created_at) VALUES ({values})
        """
        db.execute(statement=query)
        db.commit()
        return True
        
    
    def update(self, db: Session, update_data: UpdateSchema):
        """
        """
        pass
    
    def delete(self, db: Session, id: int):
        """
        """
        pass
