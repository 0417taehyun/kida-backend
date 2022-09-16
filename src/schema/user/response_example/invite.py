from src.schema.response import GetResponseModel, ErrorResponseModel


invite_user_response = {
    "200": {
        "model": GetResponseModel,
        "description": "초대장 생성 성공",
        "content": {
            "application/json": {
                "example": {
                    "data": "Invitation code"
                },       
            }
        },
    }
}
