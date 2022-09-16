from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse

from src.database import get_db
from src.crud import crud_activity
from src.util import get_seoul_culture_events, auth_user


router = APIRouter()
BASE_SINGLE_PREFIX: str = "/activity"
BASE_PLURAL_PREFIX: str = "/activities"
CATEGORY_SINGLE_PREFIX: str = BASE_SINGLE_PREFIX + "/category"
CATEGORY_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/categories"
LOCATION_SINGLE_PREFIX: str = BASE_SINGLE_PREFIX + "/location"
LOCATION_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/locations"


@router.get(BASE_SINGLE_PREFIX + "/{activity_id}")
def count_activity(
    activity_id: int = Path(
        ...,
        description="활동 페이지 조회수 측정을 위한 경로 매개변수",
        example=1
    ),
    db = Depends(get_db)
) -> JSONResponse:
    """
    
    """
    try:
        if crud_activity.count_up_activity_page_view(
            db=db, activity_id=activity_id
        ):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(BASE_PLURAL_PREFIX)
def get_activities(db=Depends(get_db)) -> JSONResponse:
    try:
        if result := crud_activity.get_multi(db=db):
            return JSONResponse(
                content={"data": result},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"deta": []},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@router.get(CATEGORY_PLURAL_PREFIX)
def get_activity_categories(db=Depends(get_db)) -> JSONResponse:
    """
    
    """
    try:
        if result := crud_activity.get_multi_category(db=db):
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


@router.get(LOCATION_PLURAL_PREFIX)
def get_activity_locationss(db=Depends(get_db)) -> JSONResponse:
    """
    
    """
    try:
        if result := crud_activity.get_multi_location(db=db):
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


@router.post(BASE_PLURAL_PREFIX)
def create_activities(db=Depends(get_db)) -> JSONResponse:
    """
    
    """
    try:
        result = get_seoul_culture_events()
        if result["status"] == "INFO-000":
            if crud_activity.bulk_create(db=db, insert_data=result["data"]):
                return JSONResponse(
                    content={"detail": "success"},
                    status_code=status.HTTP_200_OK
                )
        
        else:
            return JSONResponse(
                content={"detail": result["detail"]},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post(BASE_SINGLE_PREFIX + "/{activity_id}/like")
def like_activity(
    activity_id: int = Path(
        ...,
        description="활동 찜하기를 위한 경로 매개변수",
        example=1
    ),
    db = Depends(get_db),
    payload = Depends(auth_user)
) -> JSONResponse:
    try:
        if crud_activity.like_activity(
            db=db,
            activity_id=activity_id,
            user_id=payload.get("user_id"),
            user_type=payload.get("user_type")
        ):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
