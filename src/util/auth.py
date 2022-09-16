from jose import JWTError, jwt
from fastapi import HTTPException, status, Header, Depends
from sqlalchemy.orm import Session

from src.core import get_settings
from src.database import get_db


def auth_user(
    db: Session = Depends(get_db),
    Authorization: str = Header(..., description="사용자 계정 액세스 토큰")
):
    """
    """
    try:
        payload = jwt.decode(
            token=Authorization,
            key=get_settings().SECRET_KEY,
            algorithms=[get_settings().ALGORITHM]
        )
        user_id = payload.get("user_id")
        user_type = payload.get("user_type")
        if user_id:
            query: str = f"SELECT id FROM {user_type} WHERE id = {user_id}"
            if db.execute(statement=query).fetchone():
                return payload
            else:
                raise HTTPException(
                    detail="user not found",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
        else:
            raise HTTPException(
                detail="access token not found",
                status_code=status.HTTP_403_FORBIDDEN
            )            
        
    except JWTError as jwt_error:
        raise HTTPException(
            detail=str(jwt_error),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
