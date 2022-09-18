from pydantic import BaseModel


class BaseDiaryReply(BaseModel):
    content: str | None


class CreateDiaryReply(BaseDiaryReply):
    content: str


class UpdateDiaryReply(BaseDiaryReply):
    pass
