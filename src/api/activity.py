from fastapi import APIRouter, Request, status, Query, Path, Depends, Body
from fastapi.responses import JSONResponse

from src.crud import activity_crud, user_crud
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

@router.post(path=SINGLE_PREFIX + "/{activity_id}")
async def create_list(
    request: Request,
    activity_id: str = Path(..., description=""),
    type: str = Query("liked", description=""),
    payload = Depends(user_crud.auth_user),
):
    try:
        result = await user_crud.create_list(
            request=request,
            type=type,
            activity_id=activity_id,
            payload=payload,
        )
        return JSONResponse(
            content={"data": result},
            status_code=status.HTTP_200_OK
        )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.patch(path=PLURAL_PREFIX)
async def update(
    request: Request,
    update_data = Body(...)
):
    try:
        if await activity_crud.update(
            request=request, update_data=update_data
        ):
            return JSONResponse(
                content={"detail": "Success"},
                status_code=status.HTTP_200_OK
            )
        
        else:
            return JSONResponse(
                content={"detail": "Database Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )        