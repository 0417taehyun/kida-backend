from sqlalchemy.orm import Session

from src.model import Level, LevelType
from src.schema import CreateLevel
from src.crud.base import CRUDBase
from src.util import convert_datetime_to_string, get_current_datetime


class CRUDLevel(CRUDBase):
    pass
    # def create(self, db: Session, insert_data: CreateLevel) -> bool:
    #     converted_insert_data: dict = insert_data.dict()
        
    #     columns: str = ",".join(
    #         [ column for column in converted_insert_data.keys()]
    #     )
        
    #     values: str = ""
    #     for value in converted_insert_data.values():
    #         if isinstance(value, LevelType):
    #             value += f"\'{value.name}\',"

    #     current_datetime = convert_datetime_to_string(get_current_datetime())
    #     values += f"\'{current_datetime}\'"
        
    #     query: str = f"""
    #     INSERT INTO {self.model.__tablename__}
    #     ({columns}, 'created_at') VALUES ({values})
    #     """
    #     db.execute(statement=query)
    #     db.commit()
        
    #     return True        


crud_level = CRUDLevel(model=Level)
