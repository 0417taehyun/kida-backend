from fastapi import Request
from bson.objectid import ObjectId
from pymongo import ReturnDocument, DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateDiary, UpdateDiary, UserType
from src.util import get_datetime, convert_datetime_to_string


class CRUDDiary(CRUDBase[CreateDiary, UpdateDiary]):
    async def get_one(
        self,
        request: Request,
        id: str,
        user_type: UserType
    ):
        if user_type == "child":
            document = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(id)},
                update={"$set": {"is_child_read": True}},
                projection={
                    "parent_id": False,
                    "child_id": False,
                    "_id": False,
                    "question_id": False,
                    "created_at": False,
                    "child_answered_at": False,
                },
                return_document=ReturnDocument.AFTER
            )
            if document["parent_answered_at"]:
                document["parent_answered_at"] = convert_datetime_to_string(
                    document["parent_answered_at"], format="%y.%m.%d %H시 %M분"
                )
            
        else:
            document = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(id)},
                update={"$set": {"is_parent_read": True}},
                projection={
                    "parent_id": False,
                    "child_id": False,
                    "_id": False,
                    "question_id": False,
                    "created_at": False,
                    "child_answered_at": False,
                },
                return_document=ReturnDocument.AFTER                
            )
            if document["parent_answered_at"]:
                document["parent_answered_at"] = convert_datetime_to_string(
                    document["parent_answered_at"], format="%y.%m.%d %H시 %M분"
                )           
            
        return document
    
    async def get_multi(
        self,
        request: Request,
        user_id: str,
        user_type: UserType
    ):
        documents = await request.app.db[self.collection].find(
            filter={
                f"{user_type}_id": ObjectId(user_id),
                "is_child_answered": True,
            },
            projection={
                "parent_answer": False,
                "created_at": False,
                "parent_answered_at": False,
                "question_id": False,
                "parent_id": False,
                "child_id": False,
            }
        ).sort([("child_answered_at", DESCENDING)]).to_list(length=None)
        print(documents)
        for document in documents:
            if "child_answered_at" in document:
                document["from_today"] = (
                    get_datetime() - document.pop("child_answered_at")
                ).days
            document["_id"] = str(document["_id"])
            
        return documents
    
    async def create(
        self,
        request: Request,
        insert_data: CreateDiary
    ) -> dict:
        insert_data.question_id = ObjectId(insert_data.question_id)
        insert_data.child_id = ObjectId(insert_data.child_id)
        insert_data.parent_id = ObjectId(insert_data.parent_id)
        return await super().create(request, insert_data)

    async def update(
        self,
        request: Request,
        id: str,
        payload,
        diary_type: str,
        update_data: UpdateDiary
    ):
        user_type = payload.get("user_type")
        
        if diary_type == "activity":
            if user_type == "child":
                activity = await request.app.db["activities"].find_one(
                    filter={"_id": ObjectId(id)},
                    projection={"created_at": False}
                )
                update_data = {
                    "child_id": ObjectId(payload.get("user_id")),
                    "parent_id": ObjectId(payload.get("other_id")),
                    "question_id": activity["_id"],
                    "question_content": activity["title"],
                    "question_keyword":  None,
                    "child_answered_at": get_datetime(),
                    "parent_answered_at": None,
                    "is_child_read": False,
                    "is_parent_read": False,
                    "is_child_answered": True,
                    "is_parent_answered": False,
                    "emotion": update_data.emotion,
                    "child_answer": update_data.answer,
                    "sequence_id": None,
                    "created_at": get_datetime(),
                    "diary_type": "activity"
                }        
                result = await request.app.db[self.collection].insert_one(
                    update_data
                )

                await request.app.db["users"].find_one_and_update(
                    filter={"_id": ObjectId(payload.get("user_id"))},
                    update={"$push": {"visited": activity}},
                )
                await request.app.db["users"].find_one_and_update(
                    filter={"_id": ObjectId(payload.get("user_id"))},
                    update={"$pull": {"liked": {"_id": activity["_id"]}}},
                )     
                await request.app.db["users"].find_one_and_update(
                    filter={"_id": ObjectId(payload.get("other_id"))},
                    update={"$push": {"visited": activity}},              
                )                   
                await request.app.db["users"].find_one_and_update(
                    filter={"_id": ObjectId(payload.get("other_id"))},
                    update={"$pull": {"liked": {"_id": activity["_id"]}}},            
                )                
                
            else:
                converted_update_data: dict = update_data.dict(
                    exclude_none=True
                )
                converted_update_data["parent_answered_at"] = get_datetime()
                converted_update_data["parent_answer"] = (
                    converted_update_data.pop("answer")
                )
                converted_update_data["is_parent_answered"] = True
                result = (
                    await request.app.db[self.collection].find_one_and_update(
                        {"_id": ObjectId(id)}, {"$set": converted_update_data}
                    )
                )
            
        
        else:
            converted_update_data: dict = update_data.dict(exclude_none=True)
            if user_type == "child":
                await request.app.db["users"].find_one(
                    {"_id": payload.get("user_id")}
                )
                
                converted_update_data["child_answered_at"] = get_datetime()
                converted_update_data["child_answer"] = converted_update_data.pop(
                    "answer"
                )
                converted_update_data["is_child_answered"] = True
                result = await request.app.db[self.collection].find_one_and_update(
                    {"_id": ObjectId(id)}, {"$set": converted_update_data}
                )
            
            else:
                converted_update_data["parent_answered_at"] = get_datetime()
                converted_update_data["parent_answer"] = converted_update_data.pop(
                    "answer"
                )
                converted_update_data["is_parent_answered"] = True
                result = await request.app.db[self.collection].find_one_and_update(
                    {"_id": ObjectId(id)}, {"$set": converted_update_data}
                )
                
        return result


diary_crud = CRUDDiary(collection="diaries")