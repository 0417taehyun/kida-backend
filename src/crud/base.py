from typing import Generic, TypeVar

from bson.objectid import ObjectId
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING

from src.util import get_datetime


CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, collection: str) -> None:
        self.collection = collection
        
        
    async def get_one(self, request: Request, id: str):
        document = await request.app.db[self.collection].find_one(
            {"_id": ObjectId(id)}
        )
        document["_id"] = str(document["_id"])
    
    
    async def get_multi(self, request: Request):
        documents = await request.app.db[self.collection].find(
            projection={"created_at": False, "_id": False}
        ).to_list(length=None)
            
        return jsonable_encoder(documents)
    
    
    async def create(
        self,
        request: Request,
        insert_data: CreateSchema
    ) -> dict:
        converted_insert_data = insert_data.dict()
        converted_insert_data["created_at"] = get_datetime()
        inserted_document = await request.app.db[self.collection].insert_one(
            converted_insert_data
        )
        return inserted_document.acknowledged
    
    
    async def update(self, request: Request, update_data: UpdateSchema):
        pass
    
        
    async def delete(self, request: Request):
        pass
    