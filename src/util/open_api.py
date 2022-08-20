import re
import requests

from datetime import datetime, timezone, timedelta

from src.core import get_settings
from src.schema import CreateActivity


def get_datetime() -> datetime:
    delta = timedelta(hours=9)
    return datetime.utcnow() + delta

def convert_string_to_datetime(str_datetime: str) -> datetime:
    return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S.%f")

def convert_datetime_to_string(
    datetime: datetime, format="%Y-%m-%d %H-%M-%S"
) -> str:
    return datetime.strftime(format)

def get_seoul_culture_events(
    start_index: int = 0,
    end_index: int = 100,
    secret_key: str = get_settings().SEOUL_DATA_PORTAL_SECRET_KEY,
) -> dict:
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
            if (payment := data["PAYATNM"]) != "무료":
                payment = "유료"
                        
            title: str = re.sub(
                pattern=r"([\[\(\{].+[\]\}\)])",
                repl="",
                string=data["SVCNM"]
            ).lstrip()
            if not title:
                title = data["SVCNM"]
            result["data"].append(
                CreateActivity(
                    title=title,
                    type=data["MINCLASSNM"],
                    state=data["SVCSTATNM"],
                    payment=payment,
                    location=data["AREANM"],
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
                )
            )
    
    return result
