from fastapi import APIRouter

from src.api import activity, diary, user, question

router = APIRouter()

router.include_router(router=activity.router, tags=["체험활동"])
router.include_router(router=diary.router, tags=["일기"])
router.include_router(router=user.router, tags=["사용지"])
router.include_router(router=question.router, tags=["질문"])
