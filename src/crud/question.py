from datetime import datetime

from fastapi import Request
from bson.objectid import ObjectId
from pymongo import DESCENDING

from src.util import get_datetime
from src.crud.base import CRUDBase
from src.schema import CreateQuestion, UpdateQuestion, CreateDiary


class CRUDQuestion(CRUDBase[CreateQuestion, UpdateQuestion]):
    async def get_one(self, request: Request, payload):
        result: dict = {}

        user_type = payload.get("user_type")
        last_answered = await request.app.db["diaries"].find(
            filter={f"{user_type}_id": ObjectId(payload.get("user_id"))},
            sort=[("child_answered_at", DESCENDING)],
            limit=1
        ).to_list(length=None)
        if not last_answered:
            user = await request.app.db["users"].find_one(
                {"_id": ObjectId(payload.get("user_id"))}
            )
            if user_type == "child":
                child_id = user["_id"]
                parent_id = user["parent_id"]
            
            else:
                child_id = user["child_id"]
                parent_id = user["_id"]
                
            question = await request.app.db[self.collection].find_one(
                filter={"sequence_id": 1}
            )
            
            diary = CreateDiary(
                diary_type="answer",
                child_id=child_id,
                parent_id=parent_id,
                question_id=question["_id"],
                question_content=question["content"],
                question_keyword=question["keyword"],
                sequence_id=question["sequence_id"]                
            )
            converted_diary_data = diary.dict()
            converted_diary_data["created_at"] = get_datetime()
            document = await request.app.db["diaries"].insert_one(
                converted_diary_data
            )
            
            result["diary_id"] = str(document.inserted_id)
            result["qustion_id"] = str(question["_id"])
            result["question_content"] = question["content"]
            result["question_keyword"] = question["keyword"]    
            result["is_child_answered"] = False

        
        else:
            last_answered = last_answered[0]
            if (
                last_answered["is_child_answered"]
                and
                ((
                    datetime.now()
                    -
                    last_answered["child_answered_at"]
                ).seconds // 3600) > 24
            ):
                question = await request.app.db[self.collection].find_one(
                    filter={"sequence_id": last_answered["sequence_id"] + 1}
                )
                diary = CreateDiary(
                    diary_type="answer",
                    child_id=last_answered["child_id"],
                    parent_id=last_answered["parent_id"],
                    question_id=question["_id"],
                    question_content=question["content"],
                    questoin_keyword=question["keyword"],
                    sequence_id=question["sequence_id"]
                )
                converted_diary_data = diary.dict()
                converted_diary_data["created_at"] = get_datetime()
                document = request.app.db["diaries"].insert_one(
                    converted_diary_data
                )
                
                result["diary_id"] = str(document.inserted_id)
                result["qustion_id"] = str(question["_id"])
                result["question_content"] = question["content"]
                result["question_keyword"] = question["keyword"]  
                result["is_child_answered"] = False 


            else:
                result["diary_id"] =str(last_answered["_id"])
                result["question_id"] = str(last_answered["question_id"])
                result["question_content"] = last_answered["question_content"]
                result["question_keyword"] = last_answered["question_keyword"]
                result["is_child_answered"] = True

        
        return result
        

question_crud = CRUDQuestion(collection="questions")
