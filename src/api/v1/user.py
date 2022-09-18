from fastapi import APIRouter, Path, Query, Body, Depends, status
from fastapi.responses import JSONResponse

from src.schema import (
    GetUser,
    CreateUser,
    check_if_user_sign_up_response,
    get_invited_users_response,
    invite_user_response,
    get_activiy_likes_response,
    sign_in_response,
    sign_up_response
)
from src.database import get_db
from src.util import auth_user
from src.crud import crud_user


router = APIRouter()
BASE_SINGLE_PREFIX: str = "/user"
BASE_PLURAL_PREFIX: str = "/users"
DIARY_SINGLE_PREFIX: str = BASE_SINGLE_PREFIX + "/diary"
DIARY_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/diaries"
LIKE_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/likes"
INVITE_SINGLE_PREFIX: str = BASE_SINGLE_PREFIX + "/invite"
INVITE_PLURAL_PREFIX: str = BASE_SINGLE_PREFIX + "/invites"


@router.get(DIARY_SINGLE_PREFIX)
def get_latest_diary(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    가장 최근 생성된 일기 조회 API
    
    """
    try:
        if result := crud_user.get_latest_diary(
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
            content={"deatil": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(DIARY_SINGLE_PREFIX)
def get_specific_diary(
    diary_id: int = Path(
        ...,
        description="",
        example=""
    ),
    db=Depends(get_db),
    payload=Depends(auth_user)
) -> JSONResponse:
    """
    작성된 개별 일기 조회 API
    
    """
    try:
        return
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get(DIARY_PLURAL_PREFIX)
def get_diaries(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    작성된 일기 목록 조회 API
    
    """
    try:
        pass
    
    except Exception as error:
        return JSONResponse
    

@router.post(DIARY_SINGLE_PREFIX + "/{diary_id}")
def write_diary(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    try:
        crud_user.write_diary(db=db)
    
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    


@router.get(LIKE_PLURAL_PREFIX, responses=get_activiy_likes_response)
def get_both_activity_likes(
    db=Depends(get_db),
    payload=Depends(auth_user)
) -> JSONResponse:
    """
    찜한 활동 조회 API
    
    부무와 자녀가 찜한 활동을 조회하는 API로 응답 내부에서 users 키를 통해 누가 찜한 활동인지 구분되어 있다. \n
    이때 users 키의 값은 배열 형태로 만약 부모와 자녀 모두 찜한 경우 ["parent", "child"] 같은 형태로 전달된다.
    """
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
        
        
@router.post(LIKE_PLURAL_PREFIX + "/{activity_id}")
def visit_activity(
    activity_id: int = Path(
        ...,
        description="방문여부를 적용시키기 위한 활동의 고유 기본키(id)",
        example=1
    ),
    db=Depends(get_db),
    payload=Depends(auth_user)
) -> JSONResponse:
    """
    찜한 활동 중 방문한 활동 등록 API
    
    Path(required): activity_id \n
    
    자녀가 부모와 본인이 찜한 활동 중에서 방문한 활동에 대해 방문했음을 체크하는 API다. \n
    해당 API를 통해 성공 응답을 받아야 활동에 대해 일기를 작성하는 시나리오로 넘어갈 수 있다. \n
    이를 통해 방문 했다고 표시했는데 일기를 쓰다가 작성 취소한 경우 방문한 곳에서 일기를 쓸 수 있게 할 수 있다.
    """
    try:
        if crud_user.visit_activity(
            db=db,
            user_id=payload.get("user_id"),
            user_type=payload.get("user_type"),
            activity_id=activity_id
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
    

@router.post(BASE_SINGLE_PREFIX + "/sign-up", responses=sign_up_response)
def sign_up(
    invitation_code: str = Query(
        default=None,
        description="8자리로 구성된 고유한 초대장 번호",
        example="T8x-1Abc"
    ),
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
    
    Query(optional): invitation_code \n
    Body(required): type, user_type, account, password, nickname \n
    Body(optional): character_name \n
    
    회원가입을 위한 API로 부모와 자녀가 구분되어 있다. \n
    자녀의 경우 부모를 통해 가입하기 때문에 쿼리 파라미터로 token 값을 넘겨줘야 하며 추가적으로 바디 파라미터에서는 character_name 필드의 값을 전달해야 한다. \n
    이때 type은 부모와 자녀를 구분하는 대분류를 의미하며 user_type은 부모 중에서도 어머니와 아버지, 자녀들 또한 첫째, 둘째 등을 의미한다.
    """
    try:
        if crud_user.sign_up(
            db=db, invitation_code=invitation_code, insert_data=insert_data
        ):
            return JSONResponse(
                content={"detail": "success"},
                status_code=status.HTTP_200_OK
            )
    
    except ValueError as value_error:
        return JSONResponse(
            content={"detail": str(value_error)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        
@router.post(BASE_SINGLE_PREFIX + "/sign-in", responses=sign_in_response)
def sign_in(user_data: GetUser, db=Depends(get_db)) -> JSONResponse:
    """
    로그인 API

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

    
@router.get(
    INVITE_SINGLE_PREFIX + "/{invitation_code}",
    responses=check_if_user_sign_up_response
)
def check_if_user_sign_up(
    invitation_code: str = Path(
        ...,
        description="8자리로 구성된 고유한 초대장 번호",
        example="T8x-1Abc"
    ),
    db=Depends(get_db),
    payload=Depends(auth_user)
) -> JSONResponse:
    """
    초대장 번호를 통한 초대한 사용자의 회원가입 여부 확인 API
    
    Path(required): invitation_code \n
    
    초대장 번호를 통해 자녀의 가입 여부를 확인하는 API다. \n
    """
    try:
        if result := crud_user.check_if_user_sign_up_by_invitation_code(
            db = db,
            user_type = payload.get("user_type"),
            invitation_code = invitation_code,
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


@router.get(INVITE_PLURAL_PREFIX, responses=get_invited_users_response)
def get_invited_users(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    본인이 초대하여 가입한 사용자들 확인 API
    
    본인이 초대하여 가입한 사용자들을 확인할 수 있는 API다. \n
    """
    try:
        if result := crud_user.get_invited_users(
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


@router.get(INVITE_SINGLE_PREFIX, responses="")
def get_invitation_code(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    초대장 조회 API
    
    생성된 부모의 고유 초대장 번호를 조회하는 API다.
    """
    try:
        if result := crud_user.get_invitation_code(
            db=db, user_id=payload.get("user_id")
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


@router.post(INVITE_SINGLE_PREFIX, responses=invite_user_response)
def invite_user(
    db=Depends(get_db), payload=Depends(auth_user)
) -> JSONResponse:
    """
    초대장 생성 API
    
    초대장 생성을 위한 API로 부모는 해당 API를 통해 8자리 고유한 초대장 번호를 부여 받고 이를 통해 자녀를 가입 시킨다.
    초대를 위한 URI를 생성할 때 응답으로 전달하는 8자리 고유 초대장 번호를 사용해서 /user/sign-up API를 호출해야 정상적인 회원가입이 된다.
    """
    try:
        if result := crud_user.invite(
            db=db,
            user_type=payload.get("user_type"),
            user_id=payload.get("user_id")
        ):
            return JSONResponse(
                content={"data": result},
                status_code=status.HTTP_200_OK
            )
        
    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        