from fastapi import Request, HTTPException, status, Header
from bson.objectid import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.core import get_settings
from src.util import get_datetime
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
                encoded_data = {
                    "user_type": user["type"],
                    "user_id": str(user["_id"])
                }
                access_token = jwt.encode(
                    claims=encoded_data,
                    key=get_settings().SECRET_KEY,
                    algorithm=get_settings().ALGORITHM
                )
                return access_token

            else:
                return None
    
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
                
        
    
    
user_crud = CRUDUser(collection="users")
