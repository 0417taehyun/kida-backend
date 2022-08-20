import re

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pymongo import InsertOne

from src.crud.base import CRUDBase
from src.schema import CreateActivity, UpdateActivity
from src.util import get_datetime, convert_datetime_to_string


class CRUDActivity(CRUDBase[CreateActivity, UpdateActivity]):
    async def get_multi(self, request: Request):
        documents = await request.app.db[self.collection].find(
            filter={},
            projection={"created_at": False, "_id": False}
        ).to_list(length=None)
        for document in documents:
            for key, value in document.items():
                if re.match(pattern=r".+_date", string=key):
                    document[key] = convert_datetime_to_string(value)
            
        return jsonable_encoder(documents)
    
    async def bulk_create(
        self, request: Request, insert_data: list[CreateActivity]
    ) -> bool:
        query: list[InsertOne] = []
        for data in insert_data:
            converted_data = data.dict()
            converted_data["created_at"] = get_datetime()
            query.append(InsertOne(converted_data))

        inserted_document = await request.app.db[self.collection].bulk_write(
            query
        )
        return (
            True
            if (inserted_document.inserted_count == len(insert_data))
            else False
        )
                


activity_crud = CRUDActivity(collection="activities")
