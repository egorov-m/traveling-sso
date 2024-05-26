from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import EmailStr, constr

from ..base import SsoBaseModel


class UserRoleType(StrEnum):
    user = "user"
    admin = "admin"


class CreateUserRequestSchema(SsoBaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=255)
    username: constr(pattern=r"^[a-zA-Z0-9_]{5,32}$") | None = None


class InternalCreateUserRequestSchema(CreateUserRequestSchema):
    id: UUID | None = None
    role: UserRoleType
    passport_rf_id: UUID | None = None
    foreign_passport_rf_id: UUID | None = None


class UserSchema(SsoBaseModel):
    id: UUID
    email: EmailStr
    username: str | None = None
    role: UserRoleType
    created_at: datetime
    updated_at: datetime
    is_passport_rf: bool = False
    is_foreign_passport: bool = False


class UserSessionSchema(UserSchema):
    session_id: UUID
    client_id: str
