from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    LEVEL: str
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(env="ALGORITHM")
    
    SEOUL_DATA_PORTAL_SECRET_KEY: str

    class Config:
        env_file = ".env"
        

class DeveloperSettings(Settings):
    DB_URL: str = Field(env="DEVELOP_DB_URL")
    DB_NAME: str = Field(env="DEVELOP_DB_NAME")
    
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]


class ProductSettings(Settings):
    DB_URL: str = Field(env="PRODUCT_DB_URL")
    DB_NAME: str = Field(env="PRODUCT_DB_NAME")
    
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]


@lru_cache
def get_settings():
    if Settings().LEVEL == "DEVELOP":
        return DeveloperSettings()
    else:
        return ProductSettings()
    