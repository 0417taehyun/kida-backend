from src.schema.response import GetResponseModel, ErrorResponseModel


sign_in_response = {
    "200": {
        "model": GetResponseModel,
        "description": "로그인 성공",
        "content": {
            "application/json": {
                "example": {
                    "data": "Access Token"
                },       
            }
        },
    },
    "401": {
        "model": ErrorResponseModel,
        "description": "로그인 실패",
        "content": {
            "application/json": {
                "example": {
                    "detail": "uauthorized user"
                },       
            }            
        }
    }
    
}
