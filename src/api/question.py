from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.schema import CreateQuestion
from src.crud import question_crud

SINGLE_PREFIX = "/question"
PLURAL_PREFIX = "/questions"

router = APIRouter()


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