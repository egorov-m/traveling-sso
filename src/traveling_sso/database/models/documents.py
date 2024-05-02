from sqlalchemy import Column, String, Date, Uuid, Boolean
from uuid_extensions import uuid7

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
