from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import EmailStr, constr, Field
from starlette.responses import JSONResponse

from traveling_sso.database.utils import timestamp_to_datetime
from .user import UserSchema
from ..base import SsoBaseModel


class TokenType(StrEnum):
    Bearer = "Bearer"


class TokenResponseSchema(SsoBaseModel):
    access_token: str
    refresh_token: UUID | None = None
    token_type: TokenType = TokenType.Bearer
    expires: int = Field(..., description="Expires of refresh token.")

    def to_response_with_cookie(
            self,
            *,
            cookie_name: str,
            cookie_max_age: int,
            cookie_path: str
    ) -> JSONResponse:
        refresh_token = str(self.refresh_token)
        self.refresh_token = None
        resp = JSONResponse(content=self.model_dump())
        resp.set_cookie(
            cookie_name,
            refresh_token,
            max_age=cookie_max_age,
            expires=timestamp_to_datetime(self.expires),
            path=cookie_path,
            secure=True,
            httponly=True,
            samesite="strict"
        )

        return resp


class TokenSessionSchema(SsoBaseModel):
    session_id: UUID
    issued_at: int
    expires_at: int
    is_current: bool = False


class ClientSchema(SsoBaseModel):
    id: UUID
    client_id: str
    client_public_secret: str
    client_id_issued_at: int
    client_secret_expires_at: int
    user: UserSchema
    created_at: datetime
    updated_at: datetime


class SignInFormSchema(SsoBaseModel):
    login: EmailStr | constr(
        pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$"
    ) = Field(..., description="Username or email for login")
    password: str

    def is_email(self):
        return "@" in self.login


class SignUpFormSchema(SsoBaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=255)
