from enum import Enum
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src. model import Activity
from src.schema import (
    CreateActivity,
    UpdaetActivity,
    CreateActivityCategory,
    UpdaetActivityCategory,
    CreateActivityLocation, 
    UpdaetActivityLocation
)
from src.util import get_current_datetime, convert_datetime_to_string


class CRUDACtivity(CRUDBase[CreateActivity, UpdaetActivity]):
    def bulk_create(self, db: Session, insert_data: list) -> bool:
        for data in insert_data:
            activity: CreateActivity = data["activity"]
            activity_category: CreateActivityCategory = data["category"]
            activity_location: CreateActivityLocation = data["location"]
            current_datetime = convert_datetime_to_string(
                get_current_datetime()
            )
            
            activity_category_select_query: str = f"""
            SELECT id FROM activity_category
            WHERE name = '{activity_category.name}';
            """
            activity_category_result = db.execute(
                statement=activity_category_select_query
            ).fetchone()
            db.commit()
            
            if activity_category_result:
                activity_category_id: int = activity_category_result["id"]
            
            else:
                activity_category_insert_query: str = f"""
                INSERT INTO activity_category (name, created_at)
                VALUES ('{activity_category.name}', '{current_datetime}');
                """
                
                db.execute(statement=activity_category_insert_query)
                db.commit()
                
                activity_category_select_query: str = f"""
                SELECT id FROM activity_category
                WHERE name = '{activity_category.name}';
                """
                activity_category_result = db.execute(
                    statement=activity_category_select_query
                ).fetchone()
                db.commit()                
                
                activity_category_id: int = activity_category_result["id"]
                
            activity_location_select_query: str = f"""
            SELECT id FROM activity_location
            WHERE name = '{activity_location.name}';
            """
            activity_location_result = db.execute(
                statement=activity_location_select_query
            ).fetchone()
            db.commit()
            
            if activity_location_result:
                activity_location_id: int = activity_location_result["id"]
            
            else:
                activity_location_insert_query: str = f"""
                INSERT INTO activity_location (name, created_at)
                VALUES ('{activity_location.name}', '{current_datetime}');
                """
                
                db.execute(statement=activity_location_insert_query)
                db.commit()
                
                activity_location_select_query: str = f"""
                SELECT id FROM activity_location
                WHERE name = '{activity_location.name}';
                """
                activity_location_result = db.execute(
                    statement=activity_location_select_query
                ).fetchone()
                db.commit()                
                
                activity_location_id: int = activity_location_result["id"]
        
            converted_activity_data: dict = activity.dict(
                exclude_none=True
            )
            columns: str = ",".join(
                [ column for column in converted_activity_data.keys()]
            )
            
            values: str = ""
            for value in converted_activity_data.values():
                if isinstance(value, str):
                    values += f"\'{value}\',"
                elif isinstance(value, Enum):
                    values += f"\'{value.name}',"
                elif isinstance(value, datetime):
                    values += f"\'{convert_datetime_to_string(value)}\',"
                
                else:
                    values += f"{value},"

            activity_select_query: str = f"""
            SELECT id FROM activity
            WHERE (
                title = '{activity.title}'
                AND
                event_start_date = '{activity.event_start_date}'
            )
            """
            activity_result = db.execute(
                statement=activity_select_query
            ).fetchone()
            db.commit()
            
            if not activity_result:
                activity_insert_query: str = f"""
                INSERT INTO activity
                ({columns}, activity_category_id, activity_location_id, created_at)
                VALUES (
                    {values}
                    \'{activity_category_id}\',
                    \'{activity_location_id}\',
                    \'{current_datetime}\'
                ) ;
                """
                db.execute(statement=activity_insert_query)
                db.commit()
                
                activity_view_insert_query: str = f"""
                INSERT INTO activity_view (id, count, created_at)
                VALUES (
                    (
                        SELECT id
                        FROM activity
                        WHERE (
                            title = '{activity.title}'
                            AND
                            event_start_date = '{activity.event_start_date}'
                        )
                    ),
                    0,
                    '{current_datetime}'
                );
                """
                db.execute(statement=activity_view_insert_query)
                db.commit()
        
        return True
    
    
    def get_multi_category(self, db: Session) -> list[dict]:
        query: str = f"""
        SELECT id, name
        FROM activity_category;
        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        return jsonable_encoder(result)
    

    def get_multi_location(self, db: Session) -> list[dict]:
        query: str = f"""
        SELECT id, name
        FROM activity_location;
        """
        result = db.execute(statement=query).fetchall()
        db.commit()
        
        return jsonable_encoder(result)
    
    
    def count_up_activity_page_view(
        self, db: Session, activity_id: int
    ) -> bool:
        query: str = f"""
        UPDATE activity_view
        SET count = count + 1
        WHERE id = {activity_id}
        """
        db.execute(statement=query)
        db.commit()
        
        return True
    
    
    def like_activity(
        self,
        db: Session,
        activity_id: int,
        user_type: str,
        user_id: int
    ) -> bool:
        if user_type == "parent":
            table: str = "parent_activity_like"
            column: str = "parent_id"
        else:
            table: str = "child_activity_like"
            column: str = "child_id"
            
        select_activity_like_query: str = f"""
        SELECT id, deleted_at
        FROM {table}
        WHERE (
            {column} = {user_id}
            AND
            activity_id = {activity_id}
        );
        """
        activity_like_result = db.execute(
            statement=select_activity_like_query
        ).fetchone()
        db.commit()
        
        current_datetime = convert_datetime_to_string(get_current_datetime())
        if not activity_like_result:
            column += ",activity_id,is_visited,created_at"
            insert_activity_like_query: str = f"""
            INSERT INTO {table} ({column})
            VALUES (
                {user_id},
                {activity_id},
                0,
                '{current_datetime}'
            );
            """
            db.execute(statement=insert_activity_like_query)
            db.commit()            
        
        elif activity_like_result["deleted_at"]:
            update_activity_like_query: str = f"""
            UPDATE {table}
            SET deleted_at = NULL
            WHERE id = {activity_like_result["id"]};
            """
            db.execute(statement=update_activity_like_query)
            db.commit()

        else:
            update_activity_like_query: str = f"""
            UPDATE {table}
            SET deleted_at = '{current_datetime}'
            WHERE id = {activity_like_result["id"]};
            """
            db.execute(statement=update_activity_like_query)
            db.commit()

        
        return True
    

crud_activity = CRUDACtivity(model=Activity)