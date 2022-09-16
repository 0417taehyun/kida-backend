from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("")
def get_family():
    """
    """
    try:
        pass
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        