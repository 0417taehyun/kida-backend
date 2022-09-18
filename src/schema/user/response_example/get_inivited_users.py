from src.schema.response import GetResponseModel


get_invited_users_response = {
    "200": {
        "model": GetResponseModel,
        "description": "초대하여 가입한 사용자 목록 조회 성공",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": 25,
                            "account": "parentId",
                            "created_at": "2022-09-18T18:28:09",
                            "invitation_code": "cL9kNB_e",
                            "character_name": None
                        },
                        {
                            "id": 27,
                            "account": "parentId2",
                            "created_at": "2022-09-18T19:10:53",
                            "invitation_code": "RGrNXv8b",
                            "character_name": None
                        }
                    ]
                },       
            }
        },
    }
}
