from fastapi import APIRouter, Request, status, Query
from fastapi.responses import JSONResponse

from src.crud import activity_crud
from src.util import get_seoul_culture_events
from src.schema import PaymentType



SINGLE_PREFIX = "/activity"
PLURAL_PREFIX = "/activities"

router = APIRouter()

@router.post(path=PLURAL_PREFIX)
async def create(request: Request) -> JSONResponse:
    result = get_seoul_culture_events()
    if result["status"] == "INFO-000":
        if await activity_crud.bulk_create(
            request=request, insert_data=result["data"]
        ):
            return JSONResponse(
                content={"data": "Success"},
                status_code=status.HTTP_200_OK
            )
        
    else:
        return JSONResponse(
            content={"detail": result["detail"]},
            status_code=status.HTTP_400_BAD_REQUEST
        )

@router.get(path=PLURAL_PREFIX)
async def get_multi(
    request: Request,
    payment: PaymentType = Query(None, description="유무로 여부를 나타내는 쿼리 매개변수")
) -> JSONResponse:
    """
    활동 목록 다량 조회 API
    
    """
    result = await activity_crud.get_multi(request)
    return JSONResponse(
        content={"data": result},
        status_code=status.HTTP_200_OK,
    )
