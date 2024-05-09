from datetime import date
from typing import Literal

from sqlalchemy import Column, String, Date, Uuid, Boolean
from uuid_extensions import uuid7

from traveling_sso.shared.schemas.protocol import (
    PassportRfSchema,
    ForeignPassportRfSchema
)
from .. import Base, TimeStampMixin


class PassportRf(Base, TimeStampMixin):
    """
        Model of the passport database of the Russian Federation.
    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    series = Column(String(4), nullable=False)
    number = Column(String(6), nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)

    birth_date = Column(Date, nullable=False)
    birth_place = Column(String(255), nullable=False)

    gender = Column(String(1), nullable=False)

    issued_by = Column(String(255), nullable=False)
    division_code = Column(String(10), nullable=False)
    issue_date = Column(Date, nullable=False)
    registration_address = Column(String(255), nullable=False)

    is_verified = Column(Boolean, nullable=False)

    def to_schema(self) -> PassportRfSchema:
        return PassportRfSchema(
            series=self.series,
            number=self.number,
            first_name=self.first_name,
            last_name=self.last_name,
            second_name=self.second_name,
            birth_date=self.birth_date,
            birth_place=self.birth_place,
            gender=self.gender,
            issued_by=self.issued_by,
            division_code=self.division_code,
            issue_date=self.issue_date,
            registration_address=self.registration_address,
            is_verified=self.is_verified,
            create_at=self.created_at,
            update_at=self.updated_at
        )

    def __init__(
            self,
            *,
            series: str,
            number: str,
            first_name: str,
            last_name: str,
            birth_date: date,
            birth_place: str,
            gender: Literal["М", "Ж"],
            issued_by: str,
            division_code: str,
            issue_date: date,
            registration_address: str,
            id: str | None = None,
            second_name: str | None = None,
            is_verified: bool = False
    ):
        self.series = series
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.gender = gender
        self.issued_by = issued_by
        self.division_code = division_code
        self.issue_date = issue_date
        self.registration_address = registration_address
        self.is_verified = is_verified
        if id:
            self.id = id
        if second_name:
            self.second_name = second_name


class ForeignPassportRf(Base, TimeStampMixin):
    """
        Model of the foreign passport database of the Russian Federation.
    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    number = Column(String(20))

    first_name = Column(String, nullable=False)
    first_name_latin = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    last_name_latin = Column(String, nullable=False)
    second_name = Column(String, nullable=True)

    citizenship = Column(String(50), nullable=False)
    citizenship_latin = Column(String(50), nullable=False)

    birth_date = Column(Date, nullable=False)
    birth_place = Column(String(255), nullable=False)
    birth_place_latin = Column(String(255), nullable=False)

    gender = Column(String(1), nullable=False)

    issued_by = Column(String(255), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    is_verified = Column(Boolean, nullable=False)

    def to_schema(self) -> ForeignPassportRfSchema:
        return ForeignPassportRfSchema(
            number=self.number,
            first_name=self.first_name,
            first_name_latin=self.first_name_latin,
            last_name=self.last_name,
            last_name_latin=self.last_name_latin,
            second_name=self.second_name,
            citizenship=self.citizenship,
            citizenship_latin=self.citizenship_latin,
            birth_date=self.birth_date,
            birth_place=self.birth_place,
            birth_place_latin=self.birth_place_latin,
            gender=self.gender,
            issued_by=self.issued_by,
            issue_date=self.issue_date,
            expiry_date=self.expiry_date,
            is_verified=self.is_verified,
            create_at=self.created_at,
            update_at=self.updated_at
        )

    def __init__(
            self,
            *,
            number: str,
            first_name: str,
            first_name_latin: str,
            last_name: str,
            last_name_latin: str,
            citizenship: str,
            citizenship_latin: str,
            birth_date: date,
            birth_place: str,
            birth_place_latin: str,
            gender: Literal["М", "Ж"],
            issued_by: str,
            issue_date: date,
            expiry_date: date,
            id: str | None = None,
            second_name: str | None = None,
            is_verified: bool = False
    ):
        self.number = number
        self.first_name = first_name
        self.first_name_latin = first_name_latin
        self.last_name = last_name
        self.last_name_latin = last_name_latin
        self.citizenship = citizenship
        self.citizenship_latin = citizenship_latin
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.birth_place_latin = birth_place_latin
        self.gender = gender
        self.issued_by = issued_by
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.is_verified = is_verified
        if id:
            self.id = id
        if second_name:
            self.second_name = second_name
