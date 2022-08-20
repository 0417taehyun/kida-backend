from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse

from src.schema import CreateQuestion
from src.crud import question_crud, user_crud

SINGLE_PREFIX = "/question"
PLURAL_PREFIX = "/questions"

router = APIRouter()


@router.get(SINGLE_PREFIX)
async def get(request: Request, payload=Depends(user_crud.auth_user)):
    try:    
        if result := await question_crud.get_one(
            request=request,
            payload=payload
        ):
            return JSONResponse(
                content={"data": result},
                status_code=status.HTTP_200_OK
            )
        
        else:
            return JSONResponse(
                content={"data": []},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@router.post(SINGLE_PREFIX)
async def create(request: Request, insert_data: CreateQuestion) -> JSONResponse:
    try:
        if await question_crud.create(
            request=request, insert_data=insert_data
        ):
            return JSONResponse(
                content={"detail": "Success"},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )