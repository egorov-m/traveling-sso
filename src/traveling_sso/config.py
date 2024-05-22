from datetime import date
from functools import lru_cache
from typing import Optional, Literal
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.API_SERVERS:
            self.API_SERVERS = self._get_default_api_servers()

    PROJECT_NAME: str = "SSO"
    PROJECT_DESCRIPTION: str = "Authorization, authentication, user info microservice."
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    SSO_PROTOCOL: Literal["http", "https"] = "http"
    SSO_HOST: str = "0.0.0.0"
    SSO_PORT: int = Field(80, ge=0, le=65535)

    API_SERVERS: list = []

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
        "client_private_secret": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD"
                                 "U4LoYq/7PQUwj\nD7LHYHsqnwcT75RVzuho6tpYfLUPC4Gtzb0/358UHKzFZvG9ZjmemBNqsL2Gw8wn\n"
                                 "eZXhClJNNro9VrGFSfPHkyxhw8JncMnsNSTnRV2miLXY3LA9kvklTV3XZVsO0Y7U\nKI4k0srUI/PSDGXk"
                                 "GcKFKkMi49reTUH2iQcfnTsoKJlVE+QDltO5Rtyru7QJSS9D\nc9j9WQlzISOCevpZu0SYNP3yEeuAxNvA0"
                                 "6kRIqgroD3Lj5qb/uOn4r+1IVnuzoTG\nc/QG8Pm6bz6p9MVEpCMt07CNJYUyWj02aJp6UPsRS9P4skJ5dcj"
                                 "xxl7teDwR9YvO\n9SFowwF1AgMBAAECggEAH/MKeyF1QM3gC3MTtfC5C5CKk2dlr+s53mVBF/6/fd6Q\nO/G"
                                 "g8bEyQuZ617W3mmF5TGAuqdiU2WERhussn3XZHFWWZhZY1lRfDhj8lD+5MaUv\n6Q+g1kUG5TOnd0DIArXIR"
                                 "tzxtJ41qGezNAxSKRyp7GTo9yF9OVrUYwAQy2+/LZXM\nrDdfkF1Jk5sCWcgqkRrgFHt7JyCkAHj+Vexz/0K"
                                 "ydKOFTBXuJHSTc9v1fz/orXRs\nCYEfAhELyaaAfqTZS6VkYnNKggHa9Drjg5u7g7WoueSMa3luvxa3en0fe"
                                 "+HIqe6e\nT9jLR+C4dLoHuSD4XOR6b7ahjvIMXS4qo1pUhaR0kQKBgQDytiLtyyCXQ2GUMoRb\nmauTHjDWg"
                                 "HdlH5/yOcv+6NAe6UbpcFVVKruGvjeuaUKtDkXfQMH+zvYI2Yj09NII\noVd4KSLFUaV4BGGvz2vcULfwifY"
                                 "lxnxxke+8mRr+H+unFmbxRXt/5YR4HFekfREz\ntDDGik3VANznXNfDz3ZGizpeGwKBgQDgiHCemCJuxpIvz"
                                 "GX8JeY5cGnXC2pUgWx4\ngt5AAj70jNHztF3OI8nrpb4vsrpsoqtMF56CTWqfQB/5RV8lfIKQqmEcgIU6JP1"
                                 "W\n7hkVv4/Zn7sKhWmxsYV8TtmLJuurNURj0leGNfUAKQwDrPU94fs2+TGBI2Ch3wF4\nAQgtAbzXrwKBgQC"
                                 "PmL71nXY8yDrVKUYxw6tFMVmHrx30kE9bSmKtACUSBMZVmoaC\nCvRD9gqPf+tY49bnDTM5hE0AU2O6OZaCU"
                                 "KKljwDpaTLS3RTGpZuVD5SkFZuyIcrC\njqseFB9qNox/oLtrB8bXln1Xar1Xrj8dLgCllnISEZ6gq8dkLDw"
                                 "35Gu1/QKBgQDT\n0ML1Si3JdPg5sUhQe2xZqWufW3x+pe2vLj3+AmBjkWkKz49ixS5aaGwnUSM/EqIo\nUWv"
                                 "OHrxD6VmAbWoZ0gDV+nVMTw3f0T9RP6JYevN4aJApl7wizoZPw47ED/5o8AJJ\nbQf2a3ZqJU7ZNNPSAhpcP"
                                 "O7vlXE2o0sea1LMKoR8rwKBgAwv44qxhF9RjEqRn5PZ\naB178i/n216F+dXpGM0LrTup2TRnN8whjOB8pasl"
                                 "5aelf60ja8DRcl7Ef1NKx7XE\nFjgqXONMAjJ46cAhNJUpaSN9Ck7XHPVY3Klq70eY/l1TWx2DMTzTpOzMZCE"
                                 "FzSig\nrUueu/4b/Zovp0ELp/eld1Yz\n-----END PRIVATE KEY-----\n",
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
    SSO_ISSUERS: list[str] = ["http://localhost:33380", "http://127.0.0.1:33380"]
    ACCESS_TOKEN_EXPIRES_IN: int = 10800  # 60 * 60 * 3
    REFRESH_TOKEN_EXPIRES_IN: int = 31104000  # 60 * 60 * 24 * 30 * 12
    REFRESH_TOKEN_COOKIE_NAME: str = "sso_refresh_token"
    REFRESH_TOKEN_HEADER_NAME: str = "x-sso-refresh-token"
    REFRESH_TOKEN_COOKIE_PATH: str = "/api/v1/auth/"
    IS_REFRESH_TOKEN_VIA_COOKIE: bool = True
    ACTIVE_REFRESH_TOKEN_MAX_COUNT: int = 5
    CLIENT_ID_HEADER_NAME: str = "x-sso-client-id"
    CLIENT_SECRET_KEY_SIZE: int = Field(2048, ge=512)
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
    DB_POOL_PRE_PING: bool = True
    DB_POOL_SIZE: int = 75
    DB_MAX_OVERFLOW: int = 20

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    def get_db_url(self) -> str:
        return (f"{self.DB_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?ssl={self.DB_SSL}")

    def _get_default_api_servers(self):
        return [
            {
                "url": f"http://localhost:{self.SSO_PORT}",
                "description": "Local server"
            },
            {
                "url": f"{self.SSO_PROTOCOL}://{self.SSO_HOST}:{self.SSO_PORT}",
                "description": "Current server"
            }
        ]

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
