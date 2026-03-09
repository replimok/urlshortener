import os
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from typing import Union


class BaseConfig(BaseSettings):
    DATABASE_URL: Union[PostgresDsn, str] = "postgresql://urluser:urlpass@db:5432/urlshortener"
    SHORT_ID_LENGTH: int = 6
    MAX_URL_LENGTH: int =2048


class DevelopmentConfig(BaseConfig):
    DATABASE_URL: PostgresDsn = "postgresql://urluser:urlpass@db:5432/urlshortener"


class TestConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///./test.db"


ENV = os.getenv("ENVIRONMENT", "development")


if ENV == "test":
    config = TestConfig()
else:
    config = DevelopmentConfig()
