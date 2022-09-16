from fastapi import APIRouter, Query, Body, Depends, status
from fastapi.responses import JSONResponse

from src.schema import (
    GetUser,
    CreateUser,
    invite_user_response,
    sign_in_response,
    sign_up_response
)
from src.database import get_db
from src.util import auth_user
from src.crud import crud_user


router = APIRouter()
SINGLE_PREFIX: str = "/user"
PLURAL_PREFIX: str = "/users"


@router.get(SINGLE_PREFIX + "/likes")
def get_both_activity_likes(
    db=Depends(get_db),
    payload=Depends(auth_user)
) -> JSONResponse:
    try:
        if result := crud_user.get_activity_likes(
            db=db,
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


@router.post(SINGLE_PREFIX + "/sign-up", responses=sign_up_response)
def sign_up(
    token: str = Query(default=None, description="초대 코드", example="T8x-1Abc"),
    insert_data: CreateUser = Body(
        ...,
        description="회원가입을 위한 사용자 입력 데이터",
        example={
            "type": "mother",
            "user_type": "parent",
            "account": "parentId",
            "password": "parentPassword",
            "nickname": "nickname"
        }
    ),
    db = Depends(get_db)
) -> JSONResponse:
    """
    회원가입 API
    
    HTTP Method: POST \n
    Query(optional): token \n
    Body(required): type, user_type, account, password, nickname \n
    Body(optional): character_name \n
    
    회원가입을 위한 API로 부모와 자녀가 구분되어 있다. \n
    자녀의 경우 부모를 통해 가입하기 때문에 쿼리 파라미터로 token 값을 넘겨줘야 하며 추가적으로 바디 파라미터에서는 character_name 필드의 값을 전달해야 한다. \n
    이때 type은 부모와 자녀를 구분하는 대분류를 의미하며 user_type은 부모 중에서도 어머니와 아버지, 자녀들 또한 첫째, 둘째 등을 의미한다.
    """
    try:
        if crud_user.sign_up(db=db, token=token, insert_data=insert_data):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        
@router.post(SINGLE_PREFIX + "/sign-in", responses=sign_in_response)
def sign_in(user_data: GetUser, db=Depends(get_db)) -> JSONResponse:
    """
    로그인 API
    
    HTTP Method: POST \n
    Body(required): account, password \n
    
    로그인을 위한 API로 성공시 반환 값으로 액세스 토큰을 전달한다. \n
    이때 해당 토큰은 헤더에 Authorizaion 키에 값으로 담아 서버와 통신한다.
    """
    try:
        if access_token := crud_user.sign_in(db=db, user_data=user_data):
            return JSONResponse(
                content={"data": access_token},
                status_code=status.HTTP_200_OK,
            )
            
        else:
            return JSONResponse(
                content={"detail": "unauthorized user"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post(SINGLE_PREFIX + "/invite", responses=invite_user_response)
def invite_user(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    초대장 생성 API
    
    HTTP Method: POST \n
    
    초대장 생성을 위한 API로 부모는 해당 API를 통해 8자리 고유한 초대장 번호를 부여 받고 이를 통해 자녀를 가입 시킨다.
    초대를 위한 URI를 생성할 때 응답으로 전달하는 8자리 고유 초대장 번호를 사용해서 /user/sign-up API를 호출해야 정상적인 회원가입이 된다.
    """
    try:
        if invitation_code := crud_user.invite(
            db=db, user_id=payload.get("user_id")
        ):
            return JSONResponse(
                content={"data": invitation_code},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        