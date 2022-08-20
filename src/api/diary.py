from fastapi import APIRouter, Request, Depends, status, Path, Body, Query
from fastapi.responses import JSONResponse

from src.schema import (
    CreateDiary,
    UpdateDiary,
    DiaryType,
    get_diary_response
)
from src.crud import user_crud, diary_crud


SINGLE_PREFIX = "/diary"
PLURAL_PREFIX = "/diaries"

router = APIRouter()

@router.get(
    path=SINGLE_PREFIX + "/{diary_id}",
    responses=get_diary_response
)
async def get(
    request: Request,
    diary_id: str = Path(
        ..., description="조회하고자 하는 일기의 고유 아이디"
    ),
    payload = Depends(user_crud.auth_user)
) -> JSONResponse:
    """
    일기 개별 조회 API
    
    Header에 Authorization 키에 담긴 JWT 값을 통해 자녀인지 부모인지 판별합니다.
    이를 통해서 조회할 때 해당 질문에 대한 답변을 읽었는지 여부를 알 수 있습니다.
    """
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
    """
    일기 다량 조회 API
    
    
    """
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


@router.post(
    path=SINGLE_PREFIX + "/{id}",
)
async def write_diary(
    request: Request,
    id: str = Path(..., description="글을 쓰고자 하는 일기의 고유 아이디"),
    update_data: UpdateDiary = Body(..., description="일기 답변 내용"),
    type: DiaryType = Query("answer", ),
    payload = Depends(user_crud.auth_user)
) -> JSONResponse:
    """
    일기 작성 API
    
    Header에 Authorization 키에 담긴 JWT 값을 통해 자녀인지 부모인지 판별합니다.
    만약 자녀일 경우 필수적으로 emotion이라는 키에 감정 값을 담아서 보내줘야 합니다.
    emotion이라는 키에 올수 있는 값은 아래와 같이 다섯 가지이며 뒤에 한글은 각각의 감정에 대한 설명입니다.
    1. sad : 슬픔
    2. angry : 화남
    3. ordinary : 무표정
    4. happy : 기쁨
    5. surprised : 놀람
    """
    try:
        if await diary_crud.update(
            request=request,
            id=id,
            payload=payload,
            diary_type=type,
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


@router.delete(SINGLE_PREFIX)
async def delete(request: Request):
    try:
        from bson.objectid import ObjectId
        await diary_crud.delete(
            request=request,
            field="_id",
            value=ObjectId("6301150fac5820c7d9b564b4")
        )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    