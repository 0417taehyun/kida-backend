import re

from fastapi import Request, HTTPException, status, Header
from bson.objectid import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from pymongo import ReturnDocument

from src.core import get_settings
from src.util import get_datetime, convert_datetime_to_string
from src.crud.base import CRUDBase
from src.schema import CreateUser, UpdateUser


class CRUDUser(CRUDBase[CreateUser, UpdateUser]):
    async def auth_user(
        self, 
        request: Request,
        Authorization=Header(..., description="사용자 계정 액세스 토큰")
    ):
        try:    
            payload = jwt.decode(
                token=Authorization,
                key=get_settings().SECRET_KEY,
                algorithms=[get_settings().ALGORITHM],
            )
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(
                    detail="Access Token Not Found",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            elif not request.app.db[self.collection].find_one(
                {"id": user_id}
            ):
                raise HTTPException(
                    detail="User Not Found",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            else:
                return payload
        
        except JWTError as jwt_error:
            raise HTTPException(
                detail=str(jwt_error),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    
    async def get_one(
        self,
        request: Request,
        user_data: CreateUser
    ) -> dict | None:
        user = await request.app.db[self.collection].find_one(
            {"id": user_data.id}
        )
        if not user:
            return None
        
        else:
            password_ctx = CryptContext(
                schemes=["bcrypt"], deprecated="auto"
            )
            if password_ctx.verify(
                secret=user_data.password, hash=user["password"]
            ):
                if user["type"] == "child":
                    other_type = "parent"
                    other_id = str(user["parent_id"])
                else:
                    other_type = "child"
                    other_id = str(user["child_id"])
                    
                encoded_data = {
                    "user_type": user["type"],
                    "user_id": str(user["_id"]),
                    "other_type": other_type,
                    "other_id": other_id
                }
                access_token = jwt.encode(
                    claims=encoded_data,
                    key=get_settings().SECRET_KEY,
                    algorithm=get_settings().ALGORITHM
                )
                return access_token

            else:
                return None
    
    async def get_list(self, request: Request, type, payload):
        if type =="liked":
            my_data = await request.app.db[self.collection].find_one(
                filter={"_id": ObjectId(payload.get("user_id"))},
                projection={"created_at": False},
            )
            other_data = await request.app.db[self.collection].find_one(
                filter={"_id": ObjectId(payload.get("other_id"))},
                projection={"created_at": False}
            )
            
            temp_list: dict = {}
            like_list: list[dict] = []
            
            if my_data["liked"]:
                for data in my_data["liked"]:               
                    data["like"] = [payload.get("user_type")]
                    temp_list[str(data.pop("_id"))] = data
            
            if other_data["liked"]:
                for data in other_data["liked"]:
                    if (_id := str(data["_id"])) in temp_list:
                        temp_list[_id]["like"].append(
                            payload.get("other_type")
                        )
                    
                    else:
                        data["like"] = [payload.get("other_type")]
                        temp_list[str(data.pop("_id"))] = data
            
            if temp_list:
                for _id, data in temp_list.items():
                    for key, value in data.items():
                        if re.match(pattern=r".+_date", string=key):
                            data[key] = convert_datetime_to_string(value)                 
                    like_list.append({"_id": _id, **data})
            
            return like_list
        
        else:
            my_data = await request.app.db[self.collection].find_one(
                filter={"_id": ObjectId(payload.get("user_id"))},
                projection={"created_at": False},
            )
            other_data = await request.app.db[self.collection].find_one(
                filter={"_id": ObjectId(payload.get("other_id"))},
                projection={"created_at": False}
            )
            temp_list: dict = {}
            visit_list: list[dict] = []
            if my_data["visited"]:
                for data in my_data["visited"]:
                    temp_list[str(data.pop("_id"))] : data
            
            if other_data["visited"]:
                for data in other_data["visited"]:
                    if data["_id"] not in temp_list:
                        temp_list[str(data.pop("_id"))] = data
                        
            if temp_list:
                for _id, data in temp_list.items():
                    for key, value in data.items():
                        if re.match(pattern=r".+_date", string=key):
                            data[key] = convert_datetime_to_string(value)                 
                    visit_list.append({"_id": _id, **data})                        

            return visit_list            
            
            
    
    async def create(self, request: Request, insert_data: CreateUser) -> bool | dict | None:
        password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        insert_data.password = password_ctx.hash(secret=insert_data.password)
        if insert_data.child_id:
            document = await request.app.db[self.collection].find_one(
                {"_id": ObjectId(insert_data.child_id)}
            )
            if document:
                insert_data.child_id = ObjectId(insert_data.child_id)
                converted_insert_data = insert_data.dict()
                converted_insert_data["created_at"] = get_datetime()
                parent = await request.app.db[self.collection].insert_one(
                    converted_insert_data
                )
                result = (
                    await request.app.db[self.collection].find_one_and_update(
                        {"_id": ObjectId(insert_data.child_id)},
                        {"$set": {"parent_id": parent.inserted_id}}
                    )
                )
            
        elif insert_data.parent_id:
            document = request.app.db[self.collection].find_one(
                {"_id": ObjectId(insert_data.parent_id)}
            )
            if document:
                insert_data.parent_id = ObjectId(insert_data.parent_id)
                converted_insert_data = insert_data.dict()
                converted_insert_data["created_at"] = get_datetime()
                child = await request.app.db[self.collection].insert_one(
                    converted_insert_data
                )
                result = (
                    await request.app.db[self.collection].find_one_and_update(
                        {"_id": ObjectId(insert_data.child_id)},
                        {"$set": {"child_id": child.inserted_id}}
                    )                
                )
        
        return result

    async def create_list(
        self, request: Request, type: str, activity_id: str, payload
    ):
        if type == "liked":
            activity = await request.app.db["activities"].find_one(
                filter={"_id": ObjectId(activity_id)},
                projection={"created_at": False}
            )
            activity["like"] = payload.get("user_type")
            
            result = await request.app.db[self.collection].update_one(
                filter={"_id": ObjectId(payload.get("user_id"))},
                update={"$pull": {"liked": {"_id": activity["_id"]}}},
            )
            if not result.acknowledged:
                my_data = await request.app.db[self.collection].find_one_and_update(
                    filter={"_id": ObjectId(payload.get("user_id"))},
                    projection={"created_at": False},
                    update={"$push": {"liked": activity}},
                    return_document=ReturnDocument.AFTER
                )
                other_data = await request.app.db[self.collection].find_one(
                    filter={"_id": ObjectId(payload.get("other_id"))},
                    projection={"created_at": False},
                )    
            
            return True        
            
            # temp_list: dict = {}
            # like_list: list[dict] = []
            
            # if my_data["liked"]:
            #     for data in my_data["liked"]:               
            #         data["like"] = [payload.get("user_type")]
            #         temp_list[str(data.pop("_id"))] = data
            
            # if other_data["liked"]:
            #     for data in other_data["liked"]:
            #         if (_id := str(data["_id"])) in temp_list:
            #             temp_list[_id]["like"].append(
            #                 payload.get("other_type")
            #             )
                    
            #         else:
            #             data["like"] = [payload.get("other_type")]
            #             temp_list[str(data.pop("_id"))] = data
            
            # if temp_list:
            #     for _id, data in temp_list.items():
            #         for key, value in data.items():
            #             if re.match(pattern=r".+_date", string=key):
            #                 data[key] = convert_datetime_to_string(value)                 
            #         like_list.append({"_id": _id, **data})
            
            # return like_list
        
        else:
            activity = await request.app.db["activities"].find_one(
                {"_id": ObjectId(activity_id)},
                projection={"created_at": False}
            )
            my_data = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(payload.get("user_id"))},
                update={"$push": {"visited": activity}},
                projection={"created_at": False},
                return_document=ReturnDocument.AFTER
            )
            my_data = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(payload.get("user_id"))},
                update={"$pull": {"liked": {"_id": activity["_id"]}}},
                projection={"created_at": False},
                return_document=ReturnDocument.AFTER
            )     
            other_data = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(payload.get("other_id"))},
                update={"$push": {"visited": activity}},
                projection={"created_at": False},
                return_document=ReturnDocument.AFTER                
            )                   
            other_data = await request.app.db[self.collection].find_one_and_update(
                filter={"_id": ObjectId(payload.get("other_id"))},
                update={"$pull": {"liked": {"_id": activity["_id"]}}},
                projection={"created_at": False},
                return_document=ReturnDocument.AFTER                
            )
            
            temp_list: dict = {}
            visit_list: list[dict] = []
            if my_data["visited"]:
                for data in my_data["visited"]:
                    temp_list[str(data.pop("_id"))] : data
            
            if other_data["visited"]:
                for data in other_data["visited"]:
                    if data["_id"] not in temp_list:
                        temp_list[str(data.pop("_id"))] = data
                        
            if temp_list:
                for _id, data in temp_list.items():
                    for key, value in data.items():
                        if re.match(pattern=r".+_date", string=key):
                            data[key] = convert_datetime_to_string(value)                 
                    visit_list.append({"_id": _id, **data})                        

            return visit_list
        
    
user_crud = CRUDUser(collection="users")
