from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import EmailStr, constr, Field

from .user import UserSchema
from ..base import SsoBaseModel


class TokenType(StrEnum):
    Bearer = "Bearer"


class TokenResponseSchema(SsoBaseModel):
    access_token: str
    refresh_token: UUID
    token_type: TokenType = TokenType.Bearer
    expires_in: int = Field(..., description="Expires of refresh token.")


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
    password: constr(min_length=8, max_length=255)

    def is_email(self):
        return "@" in self.login


class SignUpFormSchema(SsoBaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=255)
