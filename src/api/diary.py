from fastapi import APIRouter, Request, Depends, status, Path, Body, Query
from fastapi.responses import JSONResponse

from src.schema import UserType, CreateDiary, UpdateDiary
from src.crud import user_crud, diary_crud


SINGLE_PREFIX = "/diary"
PLURAL_PREFIX = "/diaries"

router = APIRouter()

@router.get(path=SINGLE_PREFIX + "/{diary_id}")
async def get(
    request: Request,
    diary_id: str = Path(
        ..., description="조회하고자 하는 일기의 고유 아이디"
    ),
    payload = Depends(user_crud.auth_user)
) -> JSONResponse:
    try:
        if result := await diary_crud.get_one(
            request=request,
            id=diary_id,
            user_type=payload.get("user_type")
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

@router.get(path=PLURAL_PREFIX)
async def get_multi(
    request: Request,
    payload=Depends(user_crud.auth_user)
) -> JSONResponse:
    try:
        if result := await diary_crud.get_multi(
            request=request,
            user_id=payload.get("user_id"),
            user_type=payload.get("user_type")
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


@router.post(path=SINGLE_PREFIX + "/{diary_id}")
async def write_diary(
    request: Request,
    diary_id: str = Path(..., description="글을 쓰고자 하는 일기의 고유 아이디"),
    update_data: UpdateDiary = Body(..., description="일기 답변 내용"),
    payload = Depends(user_crud.auth_user)
) -> JSONResponse:
    try:
        if await diary_crud.update(
            request=request,
            id=diary_id,
            user_type=payload.get("user_type"),
            update_data=update_data
        ):
            return JSONResponse(
                content={"detail": "Success"},
                status_code=status.HTTP_200_OK
            )
        
        else:
            return JSONResponse(
                content={"deetail": "Database Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post(path=SINGLE_PREFIX)
async def create_diary(
    request: Request,
    insert_data: CreateDiary
) -> JSONResponse:
    try:
        if await diary_crud.create(request=request, insert_data=insert_data):
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        