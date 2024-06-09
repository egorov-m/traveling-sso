from datetime import date, datetime
from typing import Literal

from ..base import SsoBaseModel
from pydantic import constr


class CreatePassportRfResponseSchema(SsoBaseModel):
    series: constr(min_length=4, max_length=4)
    number: constr(min_length=6, max_length=6)

    first_name: str
    last_name: str
    second_name: str | None = None

    birth_date: date
    birth_place: constr(max_length=255)

    gender: Literal["М", "Ж"]

    issued_by: constr(max_length=255)
    division_code: constr(max_length=10)
    issue_date: date
    registration_address: constr(max_length=255)


class UpdatePassportRfResponseSchema(SsoBaseModel):
    series: str | None = None
    number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    second_name: str | None = None
    birth_date: date | None = None
    birth_place: str | None = None
    gender: Literal["М", "Ж"] | None = None
    issued_by: str | None = None
    division_code: str | None = None
    issue_date: date | None = None
    registration_address: str | None = None


class PassportRfSchema(CreatePassportRfResponseSchema):
    is_verified: bool
    create_at: datetime
    update_at: datetime


class CreateForeignPassportRfResponseSchema(SsoBaseModel):
    number: constr(max_length=20)

    first_name: str
    first_name_latin: str
    last_name: str
    last_name_latin: str
    second_name: str | None = None

    citizenship: constr(max_length=50)
    citizenship_latin: constr(max_length=50)

    birth_date: date
    birth_place: constr(max_length=255)
    birth_place_latin: constr(max_length=255)

    gender: Literal["М", "Ж"]

    issued_by: constr(max_length=255)
    issue_date: date
    expiry_date: date


class UpdateForeignPassportRfResponseSchema(SsoBaseModel):
    number: str | None = None
    first_name: str | None = None
    first_name_latin: str | None = None
    last_name: str | None = None
    last_name_latin: str | None = None
    second_name: str | None = None
    citizenship: str | None = None
    citizenship_latin: str | None = None
    birth_date: date | None = None
    birth_place: str | None = None
    birth_place_latin: str | None = None
    gender: Literal["М", "Ж"] | None = None
    issued_by: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None


class ForeignPassportRfSchema(CreateForeignPassportRfResponseSchema):
    is_verified: bool
    create_at: datetime
    update_at: datetime
