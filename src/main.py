import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core import get_settings
from src.api import router


app = FastAPI()

app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOW_ORIGINS,
    allow_credentials=get_settings().ALLOW_CREDENTIALS,
    allow_methods=get_settings().ALLOW_METHODS,
    allow_headers=get_settings().ALLOW_HEADERS,
)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=True
    )
    