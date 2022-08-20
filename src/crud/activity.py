import re

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pymongo import InsertOne, ASCENDING
from bson.objectid import ObjectId

from src.crud.base import CRUDBase
from src.schema import CreateActivity, UpdateActivity
from src.util import get_datetime, convert_datetime_to_string


class CRUDActivity(CRUDBase[CreateActivity, UpdateActivity]):
    async def get_multi(self, request: Request, payload):
        documents = await request.app.db[self.collection].find(
            filter={
                "$or": [
                    { "state": "접수중" },
                    { "state": "안내중" }
                ]
            },
            projection={"created_at": False}
        ).sort(
            [
                ("event_start_date", ASCENDING),
                ("reservation_start_date", ASCENDING)
            ]
        ).to_list(length=None)
        
        my_data = await request.app.db["users"].find_one(
            filter={"_id": ObjectId(payload.get("user_id"))}
        )
        if my_data:
            liked_activities = [
                liked_activity["_id"] for liked_activity in my_data["liked"]
            ]
        else:
            liked_activities = []
        
        for document in documents:
            if document["_id"] in liked_activities:
                document["is_liked"] = True
            else:
                document["is_liked"] = False
                
            document["_id"] = str(document["_id"])
            for key, value in document.items():
                if re.match(pattern=r".+_date", string=key):
                    document[key] = convert_datetime_to_string(value)
            
        return jsonable_encoder(documents)
    
    async def update(self, request: Request, update_data):
        documents = await request.app.db[self.collection].update_many(
            filter={"type": update_data["before"]},
            update={"$set": {"type": update_data["after"]}}
        )
        return documents
        
    
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
