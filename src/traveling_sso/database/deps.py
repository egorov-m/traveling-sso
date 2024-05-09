from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import (
    InternalCreateUserResponseSchema,
    CreatePassportRfResponseSchema, CreateForeignPassportRfResponseSchema
)
from .core import get_session, engine, Base
from ..config import settings
from ..managers import create_or_update_passport_rf, create_or_update_foreign_passport_rf
from ..managers.client import create_or_update_client
from ..managers.user import create_or_update_user


async def get_db():
    session: AsyncSession = get_session()
    async with session.begin() as transaction:
        yield session


async def db_metadata_create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def db_init_root_user():
    async for session in get_db():
        assert settings.ROOT_ADMIN_USER, "No user data for initialization."

        passport_rf_id = None
        foreign_passport_rf_id = None
        if settings.ROOT_ADMIN_USER_DOCUMENTS:
            passport_rf_required_keys = list(CreatePassportRfResponseSchema.__fields__.keys())
            passport_rf_required_keys.append("id")
            foreign_passport_rf_required_keys = list(CreateForeignPassportRfResponseSchema.__fields__.keys())
            foreign_passport_rf_required_keys.append("id")

            passport_rf = settings.ROOT_ADMIN_USER_DOCUMENTS.get("passport_rf")
            if passport_rf is not None:
                passport_rf_dict = dict(passport_rf)
                if all(key in passport_rf_dict for key in passport_rf_required_keys):
                    passport_rf_id = passport_rf_dict.pop("id")
                    is_verified = passport_rf_dict.pop("is_verified")
                    await create_or_update_passport_rf(
                        session=session,
                        passport_data=CreatePassportRfResponseSchema(
                            **passport_rf_dict
                        ),
                        passport_id=passport_rf_id,
                        is_verified=is_verified
                    )
            foreign_passport_rf = settings.ROOT_ADMIN_USER_DOCUMENTS.get("foreign_passport_rf")
            if foreign_passport_rf is not None:
                foreign_passport_rf_dict = dict(foreign_passport_rf)
                if all(key in foreign_passport_rf_dict for key in foreign_passport_rf_required_keys):
                    foreign_passport_rf_id = foreign_passport_rf_dict.pop("id")
                    is_verified = foreign_passport_rf_dict.pop("is_verified")
                    await create_or_update_foreign_passport_rf(
                        session=session,
                        passport_data=CreateForeignPassportRfResponseSchema(
                            **foreign_passport_rf_dict
                        ),
                        passport_id=foreign_passport_rf_id,
                        is_verified=is_verified
                    )

        user_dict = dict(settings.ROOT_ADMIN_USER)
        assert all(key in user_dict for key in ("id", "email", "username", "role", "password"))

        user = await create_or_update_user(session=session, user_data=InternalCreateUserResponseSchema(
            **settings.ROOT_ADMIN_USER,
            passport_rf_id=passport_rf_id,
            foreign_passport_rf_id=foreign_passport_rf_id
        ))

        if settings.ROOT_ADMIN_USER_CLIENT is not None:
            client_required_keys = (
                "id", "client_id", "client_private_secret",
                "client_id_issued_at", "client_secret_expires_at"
            )
            if all(key in settings.ROOT_ADMIN_USER_CLIENT for key in client_required_keys):
                await create_or_update_client(
                    session=session,
                    **settings.ROOT_ADMIN_USER_CLIENT,
                    user=user
                )
        await session.commit()
        break
