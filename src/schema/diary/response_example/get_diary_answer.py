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
                            "data": {
                                "question_content": "오늘따라 갑자기 먹고 싶은 음식이 있나요?",
                                "is_child_read": True,
                                "is_parent_read": True,
                                "is_child_answered": True,
                                "is_parent_answered": True,
                                "emotion": "happy",
                                "parent_answer": "하람아! 내일 학부모 회의 때 엄마 참석할 수 있어서 떡꼬치 사먹자~ 오늘 골 넣은 거 완전 축하해! 커서 손흥민 같은 축구 선수 되겠네 ㅎㅎ",
                                "parent_answered_at": "22.08.20 17시 49분",
                                "child_answer": "예전에 엄마가 학교 앞에서 사준 떡꼬치가 엄청 맛있었는데 오랜만에 먹고 싶다. 오늘 축구했는데 골 넣어서 기분 좋은데 상으로 사주셨으면 좋겠다."
                            }
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
