from src.schema.response import GetResponseModel


check_if_user_sign_up_response = {
    "200": {
        "model": GetResponseModel,
        "description": "초대장 번호를 통한 초대한 사용자 가입 여부 확인 성공",
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "id": 25,
                        "account": "parentId",
                        "created_at": "2022-09-18T18:28:09",
                        "invitation_code": "cL9kNB_e"
                    }
                },       
            }
        },
    }
}
