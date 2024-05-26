from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from traveling_sso.database.models import User, PassportRf, ForeignPassportRf


class _FactoryMeta(type):

    async def __call__(cls, session: AsyncSession):
        fields = {k: cls._get_value_for_field(v) for k, v in vars(cls).items() if not k.startswith("__")}
        model = fields.pop("Meta").model
        model_cls = model if isinstance(model, type) else model.__class__
        model_db = model_cls(**fields)
        session.add(model_db)
        await session.flush()

        return model_db

    @classmethod
    def _get_value_for_field(cls, v, **kwargs):
        if callable(v):
            return v(**kwargs)

        return v


class UserFactory(metaclass=_FactoryMeta):
    email = lambda: f"{uuid7()}@example.com"
    username = lambda: uuid7().hex
    password = "password"
    role = "user"

    class Meta:
        model = User


class PassportRfFactory(metaclass=_FactoryMeta):
    series = "0000"
    number = "000000"
    first_name = "Firstname"
    last_name = "Last name"
    second_name = "Second name"
    birth_date = date(2000, 1, 1)
    birth_place = "Birth place."
    gender = "Ж"
    issued_by = "Passport RF issued by a state organisation."
    division_code = "000-000"
    issue_date = date(2021, 1, 12)
    registration_address = "Passport registration address."
    is_verified = True

    class Meta:
        model = PassportRf


class ForeignPassportRfFactory(metaclass=_FactoryMeta):
    number = "00 0000000",
    first_name = "Firstname",
    first_name_latin = "Firstname",
    last_name = "LastName",
    last_name_latin = "LastName",
    second_name = "SecondName",
    citizenship = "Citizenship",
    citizenship_latin = "Citizenship",
    birth_date = date(2000, 1, 1),
    birth_place = "Birth place.",
    birth_place_latin = "Birth place.",
    gender = "Ж",
    issued_by = "Foreign passport RF issued by a state organisation.",
    issue_date = date(2022, 5, 12),
    expiry_date = date(2032, 5, 12),
    is_verified = True

    class Meta:
        model = ForeignPassportRf
