from fastapi import APIRouter

from src.api.v1 import (
    activity,
    diary,
    emotion,
    family,
    level,
    question,
    user
)


router = APIRouter(prefix="/v1")
router.include_router(router=activity.router, tags=["활동"])
router.include_router(router=emotion.router, tags=["감정"])
router.include_router(router=level.router, tags=["레벨"])
router.include_router(router=question.router, tags=["질문"])
router.include_router(router=user.router, tags=["사용자"])
