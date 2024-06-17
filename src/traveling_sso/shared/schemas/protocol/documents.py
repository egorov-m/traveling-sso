from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from ..base import SsoBaseModel
from pydantic import constr


class DocumentType(StrEnum):
    passport_rf = "passport_rf"
    foreign_passport_rf = "foreign_passport_rf"


class GetDocumentTypeSlug(StrEnum):
    passport_rf = "passport_rf"
    foreign_passport_rf = "foreign_passport_rf"
    all = "all"


class DocumentTypeSlug(StrEnum):
    passport_rf = "passport_rf"
    foreign_passport_rf = "foreign_passport_rf"


class CreatePassportRfResponseSchema(SsoBaseModel):
    series: constr(min_length=4, max_length=4)
    number: constr(min_length=6, max_length=6)

    first_name: constr(max_length=512)
    last_name: constr(max_length=512)
    second_name: constr(max_length=512) | None = None

    birth_date: date
    birth_place: constr(max_length=255)

    gender: Literal["М", "Ж"]

    issued_by: constr(max_length=255)
    division_code: constr(max_length=10)
    issue_date: date
    registration_address: constr(max_length=255)


class UpdatePassportRfResponseSchema(SsoBaseModel):
    series: constr(min_length=4, max_length=4) | None = None
    number: constr(min_length=6, max_length=6) | None = None
    first_name: constr(max_length=512) | None = None
    last_name: constr(max_length=512) | None = None
    second_name: constr(max_length=512) | None = None
    birth_date: date | None = None
    birth_place: constr(max_length=255) | None = None
    gender: Literal["М", "Ж"] | None = None
    issued_by: constr(max_length=255) | None = None
    division_code: constr(max_length=10) | None = None
    issue_date: date | None = None
    registration_address: constr(max_length=255) | None = None


class PassportRfSchema(CreatePassportRfResponseSchema):
    is_verified: bool
    create_at: datetime
    update_at: datetime


class CreateForeignPassportRfResponseSchema(SsoBaseModel):
    number: constr(max_length=20)

    first_name: constr(max_length=512)
    first_name_latin: constr(max_length=512)
    last_name: constr(max_length=512)
    last_name_latin: constr(max_length=512)
    second_name: constr(max_length=512) | None = None

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
    number: constr(max_length=20) | None = None
    first_name: constr(max_length=512) | None = None
    first_name_latin: constr(max_length=512) | None = None
    last_name: constr(max_length=512) | None = None
    last_name_latin: constr(max_length=512) | None = None
    second_name: constr(max_length=512) | None = None
    citizenship: constr(max_length=50) | None = None
    citizenship_latin: constr(max_length=50) | None = None
    birth_date: date | None = None
    birth_place: constr(max_length=255) | None = None
    birth_place_latin: constr(max_length=255) | None = None
    gender: Literal["М", "Ж"] | None = None
    issued_by: constr(max_length=255) | None = None
    issue_date: date | None = None
    expiry_date: date | None = None


class ForeignPassportRfSchema(CreateForeignPassportRfResponseSchema):
    is_verified: bool
    create_at: datetime
    update_at: datetime
