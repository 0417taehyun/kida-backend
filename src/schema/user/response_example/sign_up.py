from src.schema.response import GetResponseModel


sign_up_response = {
    "200": {
        "model": GetResponseModel,
        "description": "회원가입 성공",
        "content": {
            "application/json": {
                "example": {
                    "detail": "success"
                },       
            }
        },
    }
}
