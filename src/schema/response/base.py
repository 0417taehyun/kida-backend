from pydantic import BaseModel


class GetResponseModel(BaseModel):
    """
    조회 응답 관련 스키마
    """

    data: list[dict] | dict[str, str | int] | None


class AlterResponseModel(BaseModel):
    """
    수정 및 생성 응답 관련 스키마
    """

    detail: str


class ErrorResponseModel(BaseModel):
    """
    오류 응답 관련 스키마
    """

    detail: str | list[dict[str, str]]


create_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example": {"detail": "success"}
            }
        },
    }
}

update_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "앤티티 수정",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {"detail": "success"},
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []},
                    }
                }
            }
        },
    }
}

delete_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "엔티티 삭제",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {"detail": "success"}
                    },
                    "Not Found": {
                        "summary": "데이트베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []}
                    }
                },
            }
        },
    },
}
