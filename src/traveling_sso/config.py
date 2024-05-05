from datetime import date
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

    INIT_ROOT_ADMIN_USER: bool = True

    ROOT_ADMIN_USER: Optional[dict] = {
        "id": "af5b620f-ecb5-40a6-ad5b-0a87a3bf9ff3",
        "email": "admin@example.com",
        "username": "admin",
        "role": "admin",
        "password": "123456789"
    }
    ROOT_ADMIN_USER_CLIENT: Optional[dict] = {
        "id": "77961ae0-25f3-4ec0-ac80-6e62d69f4f8c",
        "client_id": "Rh4ZomeoWHFJus8KbspWqJTtXHcMGkLHAZ30qgCD3RK3rTHJ",
        "client_public_secret": "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwS"
                                "AJBALSbdETaZPiPf7nGWpha0h4zjIm8OOiD\nArop3DvbDtwwVs9xUK+cA"
                                "Fk++3c3jfj2Zghcv/Mm2Lenn3SsTnF6OZ8CAwEAAQ==\n-----END PUBLIC KEY-----\n",
        "client_private_secret": "-----BEGIN PRIVATE KEY-----\nMIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8A"
                                 "gEAAkEAtJt0RNpk+I9/ucZa\nmFrSHjOMibw46IMCuincO9sO3DBWz3FQr5wAWT77dzeN+P"
                                 "ZmCFy/8ybYt6efdKxO\ncXo5nwIDAQABAkAXOG1odNPKiViYoAIB2JtvOp11D/gZHM769Gr"
                                 "WX0G32V/HsBIc\nnGXGDUxjZJ+XwfmAoWNsOVyfDYImnFh7r2URAiEA5WFDLkd+v4evsUOyt"
                                 "EcFOdTZ\ngoYYtAUkUrbjMWSvnLUCIQDJkS9bFD56xioLC88imcViUuaWhKsxgYhtnHi/9UeF\n"
                                 "gwIhANCwGbf8MfO9Vfo3tllQGBASd8XJjKYT24UpgTAKA7/VAiEAlFDXVp5TxwVP\nZGdhF+WsH"
                                 "sg/Udv3F+tnVrg/BYhXAz8CIQDNiEDhdct/2OpxUUJSC1fzhhxfjXo/\nfEcFr2WR5oN9Ww==\n"
                                 "-----END PRIVATE KEY-----\n",
        "client_id_issued_at": 1714913401,
        "client_secret_expires_at": 4868513467
    }
    ROOT_ADMIN_USER_DOCUMENTS: Optional[dict] = {
        "passport_rf": {
            "id": "b212aab4-7ef8-4732-83dc-14bdc4c69c7e",
            "series": "0000",
            "number": "000000",
            "first_name": "AdminFirstname",
            "last_name": "AdminLastName",
            "second_name": "AdminSecondName",
            "birth_date": date(2000, 1, 1),
            "birth_place": "Admin birth place.",
            "gender": "М",
            "issued_by": "Admin passport RF issued by a state organisation.",
            "division_code": "000-000",
            "issue_date": date(2021, 1, 12),
            "registration_address": "Admin passport registration address.",
            "is_verified": True
        },
        "foreign_passport_rf": {
            "id": "dd65dff8-9ca7-4bd0-89dc-e407ee84b36a",
            "number": "00 0000000",
            "first_name": "AdminFirstname",
            "first_name_latin": "AdminFirstname",
            "last_name": "AdminLastName",
            "last_name_latin": "AdminLastName",
            "second_name": "AdminSecondName",
            "citizenship": "Admin user citizenship",
            "citizenship_latin": "Admin user citizenship",
            "birth_date": date(2000, 1, 1),
            "birth_place": "Admin birth place.",
            "birth_place_latin": "Admin birth place.",
            "gender": "М",
            "issued_by": "Admin foreign passport RF issued by a state organisation.",
            "issue_date": date(2022, 5, 12),
            "expiry_date": date(2032, 5, 12),
            "is_verified": True
        }
    }

    AUTH_PASSWORD_SALT: str = "password-salt"

    CLIENT_SECRET_KEY_SIZE: int = Field(512, ge=512)
    CLIENT_SECRET_EXPIRES_DAYS_IN: int = 1095  # 3 years
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
