import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.core import get_settings
from src.api import router


app = FastAPI()

app.include_router(router=router)

@app.on_event("startup")
def get_database() -> None:
    app.db_client = AsyncIOMotorClient(get_settings().DB_URL)
    app.db = app.db_client[get_settings().DB_NAME]


@app.on_event("shutdown")
def close_db_connection() -> None:
    app.db_client.close()


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
    