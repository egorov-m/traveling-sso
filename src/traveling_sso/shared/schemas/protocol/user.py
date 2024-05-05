from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Secret, constr

from ..base import SsoBaseModel


class UserRoleType(StrEnum):
    user = "user"
    admin = "admin"


class CreateUserResponseSchema(SsoBaseModel):
    email: EmailStr
    password: Secret[constr(min_length=8, max_length=255)]
    username: Optional[str] = None


class InternalCreateUserResponseSchema(CreateUserResponseSchema):
    id: UUID
    role: UserRoleType
    passport_rf_id: Optional[UUID] = None,
    foreign_passport_rf_id: Optional[UUID] = None


class UserSchema(SsoBaseModel):
    id: UUID
    email: EmailStr
    username: Optional[str] = None
    role: UserRoleType
    created_at: datetime
    updated_at: datetime
