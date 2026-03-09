import os
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from typing import Union


class BaseConfig(BaseSettings):
    DATABASE_URL: Union[PostgresDsn, str] = "postgresql://urluser:urlpass@localhost:5432/urlshortener"
    SHORT_ID_LENGTH: int = 6


class TestConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///./test.db"


ENV = os.getenv("ENVIRONMENT", "prod")

# for now base is for alembic, test for tests, and prod (same alembic but loads in container from env file)
if ENV == "test":
    config = TestConfig()
else:
    config = BaseConfig()
