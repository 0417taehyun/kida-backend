from pydantic import BaseModel


class GetResponseModel(BaseModel):
    """
    조회 응답 관련 스키마
    """

    data: list[dict] | dict[str, str | int] | None
