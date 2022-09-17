from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.crud import crud_emotion
from src.schema import CreateEmotion
from src.database import get_db


router = APIRouter()
SINGLE_PREFIX: str = "/emotion"
PLURAL_PREFIX: str = "/emotions"


@router.get(PLURAL_PREFIX)
def get_emotions(db=Depends(get_db)) -> JSONResponse:
    """
    전체 감정 조회 API
    """
    try:
        if result := crud_emotion.get_multi(db=db):
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
def create_emotion(
    insert_data: CreateEmotion, db = Depends(get_db)
) -> JSONResponse:
    """
    
    """
    try:
        if crud_emotion.create(db=db, insert_data=insert_data):
            return JSONResponse(
                content={"detail" : "success"},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    