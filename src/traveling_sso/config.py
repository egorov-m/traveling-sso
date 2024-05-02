from functools import lru_cache
from typing import Optional
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SSO"
    PROJECT_DESCRIPTION: str = "Authorization, authentication, user info microservice."
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    API_SERVERS: list = [
        {
            "url": "http://localhost:33380",
            "description": "Local server"
        }
    ]

    LOG_LEVEL: str = "INFO"
    LOGGER_NAME: str = "logger.traveling_sso"
    DEBUG: bool = True

    CSRF_SECRET: Optional[str] = None

    DB_SCHEMA: str = "postgresql"
    DB_HOST: str = "sso-postgres"
    DB_PORT: str = "5432"
    DB_SSL: str = "prefer"  # disable, allow, prefer, require, verify-ca, verify-full
    DB_DRIVER: str = "asyncpg"
    DB_NAME: str = Field("project.traveling_sso", alias="POSTGRES_DB")
    DB_USER: str = Field("user.traveling_sso", alias="POSTGRES_USER")
    DB_PASSWORD: str = Field("postgres", alias="POSTGRES_PASSWORD")
    DB_POOL_SIZE: int = 75
    DB_MAX_OVERFLOW: int = 20

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    def get_db_url(self) -> str:
        return (f"{self.DB_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?ssl={self.DB_SSL}")

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
