import re
import requests

from datetime import datetime, timedelta

from src.core import get_settings
from src.util.time_converter import convert_string_to_datetime
from src.schema import (
    CreateActivity, CreateActivityLocation, CreateActivityCategory
)


def get_seoul_culture_events(
    start_index: int = 0,
    end_index: int = 100,
    secret_key: str = get_settings().SEOUL_DATA_PORTAL_SECRET_KEY,
) -> list[dict]:
    BASE_URL: str = "http://openAPI.seoul.go.kr:8088/"
    response = requests.get(
        url = (
            BASE_URL
            +
            secret_key
            +
            f"/json/ListPublicReservationCulture/{start_index}/{end_index}"
        )
    ).json()["ListPublicReservationCulture"]
    status = response["RESULT"]["CODE"]
    result: dict[str] = {"status": status}
    if status != "INFO-000":
        result["detail"] = response["RESULT"]["MESSAGE"]
        
    else:
        result["data"]: list[dict] = []
        for data in response["row"]:
            if data["PAYATNM"] == "무료":
                payment: str = "free"
            else:
                payment: str = "cost"

            category_name: str = re.sub(
                pattern=r"\/",
                repl="",
                string=data["MINCLASSNM"]
            )
            
            schema: dict = {
                "activity": CreateActivity(
                    title=data["SVCNM"],
                    payment=payment,
                    place=data["PLACENM"],
                    reservation_start_date=convert_string_to_datetime(
                        str_datetime=data["RCPTBGNDT"]
                    ),
                    reservation_end_date=convert_string_to_datetime(
                        str_datetime=data["RCPTENDDT"]
                    ),
                    event_start_date=convert_string_to_datetime(
                        str_datetime=data["SVCOPNBGNDT"]
                    ),
                    event_end_date=convert_string_to_datetime(
                        str_datetime=data["SVCOPNENDDT"]
                    ),                    
                    image_url=data["IMGURL"],
                    page_url=data["SVCURL"],
                    target=data["USETGTINFO"],
                    geo_location_x=float(data["X"]),
                    geo_location_y=float(data["Y"])
                ),
                "location": CreateActivityLocation(
                    name=data["AREANM"]
                ),
                "category": CreateActivityCategory(
                    name=category_name
                )
            }    
            
            result["data"].append(schema)

    
    return result
