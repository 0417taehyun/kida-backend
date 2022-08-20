from src.schema.response_base import GetResponseModel

get_diary_response = {
    "200": {
        "model": GetResponseModel,
        "description": "엔티티 조회",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {
                            "data": [
                                {
                                    "_id": "63009f56b7f456d0f8750fcb",
                                    "question_content": "오늘따라 갑자기 먹고 싶은 음식이 있나요?",
                                    "is_child_read": False,
                                    "is_parent_read": False,
                                    "is_child_answered": True,
                                    "is_parent_answered": True,
                                    "emotion": "happy",
                                    "child_answer": "예전에 엄마가 학교 앞에서 사준 떡꼬치가 엄청 맛있었는데 오랜만에 먹고 싶다. 오늘 축구했는데 골 넣어서 기분 좋은데 상으로 사주셨으면 좋겠다.",
                                    "from_today": 0
                                }                                
                            ]
                        }
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []}
                    }
                }
            }
        },
    },
}
