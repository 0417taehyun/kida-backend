from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.crud import user_crud
from src.schema import CreateUser


SINGLE_PREFIX = "/user"
PLURAL_PREFIX = "/users"

router = APIRouter()


@router.post(path=SINGLE_PREFIX + "/sign-in")
async def sign_in(request: Request, user_data: CreateUser):
    try:
        if result := await user_crud.get_one(
            request=request, user_data=user_data
        ):
            return JSONResponse(
                content={"data": result},
                status_code=status.HTTP_200_OK
            )
        
        else:
            return JSONResponse(
                content={"data": []},
                status_code=status.HTTP_200_OK,
            )
        
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@router.post(path=SINGLE_PREFIX + "/sign-up")
async def sign_up(request: Request, insert_data: CreateUser):
    try:
        if await user_crud.create(
            request=request, insert_data=insert_data
        ):
            return JSONResponse(
                content={"detail": "Success"},
                status_code=status.HTTP_200_OK,
            )
        
        else:
            return JSONResponse(
                content={"detail": "Database Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )