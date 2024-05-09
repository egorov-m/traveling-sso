from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, constr
from uuid_extensions import uuid7

from ..base import SsoBaseModel


class UserRoleType(StrEnum):
    user = "user"
    admin = "admin"


class CreateUserResponseSchema(SsoBaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=255)
    username: Optional[str] = None


class InternalCreateUserResponseSchema(CreateUserResponseSchema):
    id: UUID = uuid7()
    role: UserRoleType
    passport_rf_id: Optional[UUID] = None
    foreign_passport_rf_id: Optional[UUID] = None


class UserSchema(SsoBaseModel):
    id: UUID
    email: EmailStr
    username: Optional[str] = None
    role: UserRoleType
    created_at: datetime
    updated_at: datetime
    is_passport_rf: bool = False
    is_foreign_passport: bool = False
