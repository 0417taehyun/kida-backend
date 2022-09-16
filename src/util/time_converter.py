from datetime import datetime, timedelta


def get_current_datetime() -> datetime:
    delta = timedelta(hours=9)
    return datetime.utcnow() + delta


def convert_string_to_datetime(str_datetime: str) -> datetime:
    return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S.%f")


def convert_datetime_to_string(
    datetime: datetime, format="%Y-%m-%d %H-%M-%S"
) -> str:
    return datetime.strftime(format)
