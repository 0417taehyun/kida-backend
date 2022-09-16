from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db
from src.crud import crud_question
from src.schema import CreateQuestion, CreateQuestionCategory


router = APIRouter()
BASE_SINGLE_PREFIX: str = "/question"
BASE_PLURAL_PREFIX: str = "/questions"
CATEGORY_SINGLE_PREFIX: str = BASE_SINGLE_PREFIX + "/category"
CATEGORY_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/categories"


@router.post(BASE_SINGLE_PREFIX)
def create_question(
    insert_data: CreateQuestion, db = Depends(get_db), 
) -> JSONResponse:
    """
    
    """
    try:
        if crud_question.create_question(db=db, insert_data=insert_data):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(CATEGORY_SINGLE_PREFIX)
def create_question_category(
    insert_data: CreateQuestionCategory, db = Depends(get_db)
) -> JSONResponse:
    """
    
    """
    try:
        if crud_question.create_category(db=db, insert_data=insert_data):
                return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
