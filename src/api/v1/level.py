from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse

from src.crud import crud_level
from src.util import crud_file
from src.schema import CreateLevel
from src.database import get_db


router = APIRouter()
SINGLE_PREFIX: str = "/level"
PLURAL_PREFIX: str = "/levels"


@router.post(SINGLE_PREFIX)
async def create_level(request: Request, db=Depends(get_db)) -> JSONResponse:
    """
    
    """
    try:
        form_data = await request.form()
        insert_data = crud_file.parse_formdata(
            form_data=form_data, schema=CreateLevel
        )
        if crud_level.create(db=db, insert_data=insert_data):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        