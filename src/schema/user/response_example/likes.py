from src.schema.response import GetResponseModel


get_activiy_likes_response = {
    "200": {
        "model": GetResponseModel,
        "description": "부모와 자녀 찜한 활동 목록 조회",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "부모와 자녀가 찜한 활동 목록이 존재할 경우",
                        "value": {
                            "data": [
                                {
                                    "users": [
                                        "parent",
                                        "child"
                                    ],
                                    "id": 96,
                                    "created_at": "2022-09-16T10:41:46",
                                    "updated_at": None,
                                    "deleted_at": None,
                                    "activity_category_id": 1,
                                    "activity_location_id": 1,
                                    "title": "2022년 &lt;느낌 있는 박물관&gt; 교육생 모집 안내",
                                    "payment": "FREE",
                                    "page_url": "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S220214095211965696",
                                    "place": "서울역사박물관",
                                    "reservation_start_date": "2022-02-16T10:00:00",
                                    "reservation_end_date": "2022-03-08T17:00:00",
                                    "event_start_date": "2022-02-16T00:00:00",
                                    "event_end_date": "2022-11-24T00:00:00",
                                    "target": " 장애인(중고등학교 특수학급 단체(20명 이내))",
                                    "image_url": "https://yeyak.seoul.go.kr/web/common/file/FileDown.do?file_id=1644802638448LSYS43F6BEXPF9SY2Y1LF8YSN",
                                    "geo_location_x": 126.97,
                                    "geo_location_y": None
                                },
                                {
                                    "users": [
                                        "child"
                                    ],
                                    "id": 102,
                                    "created_at": "2022-09-16T10:41:46",
                                    "updated_at": None,
                                    "deleted_at": None,
                                    "activity_category_id": 1,
                                    "activity_location_id": 2,
                                    "title": "[청계천박물관] 2022년 하반기 온라인 교육 프로그램 &#39;톡톡톡 청계천&#39; 참여 기관 모집",
                                    "payment": "FREE",
                                    "page_url": "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S220516091242515755",
                                    "place": "청계천박물관(서울역사박물관 분관)",
                                    "reservation_start_date": "2022-05-16T17:00:00",
                                    "reservation_end_date": "2022-05-31T16:00:00",
                                    "event_start_date": "2022-05-16T00:00:00",
                                    "event_end_date": "2022-11-02T00:00:00",
                                    "target": " 어린이(지역아동센터 및 초등 돌봄교실 등 어린이 단체, 초등1~3학년)",
                                    "image_url": "https://yeyak.seoul.go.kr/web/common/file/FileDown.do?file_id=1652674227907NJ0HWXHSQG86GK1RZ44GJK5UV",
                                    "geo_location_x": 127.035,
                                    "geo_location_y": None
                                },
                                {
                                    "users": [
                                        "child"
                                    ],
                                    "id": 104,
                                    "created_at": "2022-09-16T10:41:46",
                                    "updated_at": None,
                                    "deleted_at": None,
                                    "activity_category_id": 1,
                                    "activity_location_id": 2,
                                    "title": "[청계천박물관] 2022년 하반기 온라인 교육 프로그램 &#39;톡톡톡 청계천&#39; 참여 기관 추가모집",
                                    "payment": "FREE",
                                    "page_url": "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S220613095832391622",
                                    "place": "청계천박물관(서울역사박물관 분관)",
                                    "reservation_start_date": "2022-06-13T11:00:00",
                                    "reservation_end_date": "2022-06-30T17:00:00",
                                    "event_start_date": "2022-06-13T00:00:00",
                                    "event_end_date": "2022-11-02T00:00:00",
                                    "target": " 어린이(지역아동센터 및 초등 돌봄교실 등 어린이 단체, 초등1~3학년)",
                                    "image_url": "https://yeyak.seoul.go.kr/web/common/file/FileDown.do?file_id=1655082246347DLNBBHTKRWKAGC5PQ07D88MQ5",
                                    "geo_location_x": 127.035,
                                    "geo_location_y": None
                                }
                            ]
                        }
                    },
                    "Not Found": {
                        "summary": "부모와 자녀 모두 찜한 활동 목록이 전혀 없을 경우",
                        "value": { "data": [] }
                    }
                },       
            }
        },
    }
}
