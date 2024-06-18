from datetime import date, timedelta
from inspect import isawaitable

from authlib.common.security import generate_token
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from traveling_sso.config import settings
from traveling_sso.database.models import User, PassportRf, ForeignPassportRf, Client, TokenSession
from traveling_sso.database.utils import utcnow
from traveling_sso.managers.client import generate_pair_secrets_keys
from traveling_sso.shared.schemas.protocol import TokenType


class _FactoryMeta(type):

    async def __call__(cls, session: AsyncSession, **kwargs):
        _fields = dict(vars(cls))
        _meta_cls = cls._get_factory_meta_cls(_fields)
        cls._check_required_fields(_meta_cls, kwargs)
        fields = {
            k: await cls._get_value_for_field(v, session=session) if kwargs.get(k) is None else kwargs.get(k)
            for k, v in _fields.items() if not k.startswith("__")
        }
        model = _meta_cls.model
        model_cls = model if isinstance(model, type) else model.__class__
        model_db = model_cls(**fields)
        session.add(model_db)
        await session.flush()

        return model_db

    @classmethod
    async def _get_value_for_field(cls, v, **kwargs):
        session = kwargs.pop("session")
        if v.__class__ == _FactoryMeta:
            return await v(session=session, **kwargs)
        if isawaitable(v):
            return await v(**kwargs)
        if callable(v):
            return v(**kwargs)

        return v

    @classmethod
    def _get_factory_meta_cls(cls, fields: dict) -> type:
        meta_cls = fields.pop("Meta", None)
        if meta_cls is None:
            raise NotImplementedError("The `Meta` class must be implemented in the factory class.")

        return meta_cls

    @classmethod
    def _check_required_fields(cls, factory_meta_cls: type, fields):
        if hasattr(factory_meta_cls, "required_fields"):
            required_fields = factory_meta_cls.required_fields
            if not all(field in fields for field in required_fields):
                raise NotImplementedError(
                    f"The fields need to be passed to the `{cls.__name__}` factory: {', '.join(required_fields)}."
                )


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
    number = "00 0000000"
    first_name = "Firstname"
    first_name_latin = "Firstname"
    last_name = "LastName"
    last_name_latin = "LastName"
    second_name = "SecondName"
    citizenship = "Citizenship"
    citizenship_latin = "Citizenship"
    birth_date = date(2000, 1, 1)
    birth_place = "Birth place."
    birth_place_latin = "Birth place."
    gender = "Ж"
    issued_by = "Foreign passport RF issued by a state organisation."
    issue_date = date(2022, 5, 12)
    expiry_date = date(2032, 5, 12)
    is_verified = True

    class Meta:
        model = ForeignPassportRf


class ClientFactory(metaclass=_FactoryMeta):
    client_id = lambda: generate_token(48)
    client_private_secret = generate_pair_secrets_keys()[1]
    client_id_issued_at = int(utcnow().timestamp())
    client_secret_expires_at = int(
        (utcnow() + timedelta(days=settings.CLIENT_SECRET_EXPIRES_DAYS_IN)).timestamp()
    )
    user = UserFactory

    class Meta:
        model = Client


class TokenSessionFactory(metaclass=_FactoryMeta):
    client_id = None
    token_type = str(TokenType.Bearer)
    refresh_token = lambda: str(uuid7())
    refresh_token_revoked_at = None
    expires_in = settings.REFRESH_TOKEN_EXPIRES_IN
    user = UserFactory

    class Meta:
        model = TokenSession
        required_fields = ("client_id",)
