from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import (
    PassportRfSchema,
    ForeignPassportRfSchema,
    CreatePassportRfResponseSchema,
    CreateForeignPassportRfResponseSchema,
    UpdatePassportRfResponseSchema
)
from traveling_sso.shared.schemas.exceptions import (
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception
)
from ..database.models import PassportRf, User, ForeignPassportRf


async def get_passport_rf_by_user_id(*, session: AsyncSession, user_id) -> PassportRfSchema | None:
    passport = await _get_passport_rf_by_user_id(session, user_id)

    if passport is not None:
        return passport.to_schema()


async def _get_passport_rf_by_user_id(session: AsyncSession, user_id):
    query = (select(PassportRf)
             .join(User, User.passport_rf_id == PassportRf.id)
             .where(User.id == str(user_id))).returning(PassportRf)
    passport = (await session.execute(query)).scalar()

    return passport


async def _get_passport_rf_by_id(session: AsyncSession, passport_id):
    query = select(PassportRf).where(PassportRf.id == passport_id)
    passport = (await session.execute(query)).scalar()

    return passport


async def get_foreign_passport_rf_by_user_id(*, session: AsyncSession, user_id) -> ForeignPassportRfSchema | None:
    passport = await _get_foreign_passport_rf_by_user_id(session, user_id)

    if passport is not None:
        return passport.to_schema()


async def _get_foreign_passport_rf_by_user_id(session: AsyncSession, user_id):
    query = (select(ForeignPassportRf)
             .join(User, User.foreign_passport_rf == ForeignPassportRf.id)
             .where(User.id == str(user_id))).returning(ForeignPassportRf)
    passport = (await session.execute(query)).scalar()

    return passport


async def _get_foreign_passport_rf_by_id(session: AsyncSession, passport_id):
    query = select(ForeignPassportRf).where(ForeignPassportRf.id == passport_id)
    passport = (await session.execute(query)).scalar()

    return passport


async def create_or_update_passport_rf(
        *,
        session: AsyncSession,
        passport_data: CreatePassportRfResponseSchema | UpdatePassportRfResponseSchema,
        passport_id: str | None = None,
        user_id: str | None = None,
        is_verified: bool = False
) -> PassportRfSchema:
    assert passport_id is None or user_id is None, "Use one of the identifiers for the search."

    passport = None
    if passport_id is not None or user_id is not None:
        if passport_id is not None:
            passport = await _get_passport_rf_by_id(session, passport_id)
        else:
            passport = await _get_passport_rf_by_user_id(session, user_id)
        if passport is not None:
            _update_passport_fields(passport=passport, fields=passport_data.model_dump())
    if passport is None:
        passport = PassportRf(
            **passport_data.model_dump(),
            id=passport_id,
            is_verified=is_verified
        )

    try:
        session.add(passport)
        await session.flush()
    except DatabaseError as error:
        raise passport_rf_not_specified_exception from error
    return passport.to_schema()


async def create_or_update_foreign_passport_rf(
        *,
        session: AsyncSession,
        passport_data: CreateForeignPassportRfResponseSchema,
        passport_id: str | None = None,
        user_id: str | None = None,
        is_verified: bool = False
) -> ForeignPassportRfSchema:
    assert passport_id is None or user_id is None, "Use one of the identifiers for the search."

    passport = None
    if (passport_id is not None or user_id is not None) or isinstance(passport_data, UpdatePassportRfResponseSchema):
        if passport_id is not None:
            passport = await _get_foreign_passport_rf_by_id(session, passport_id)
        else:
            passport = await _get_foreign_passport_rf_by_user_id(session, user_id)
        if passport is not None:
            _update_passport_fields(passport=passport, fields=passport_data.model_dump())
    if passport is None:
        passport = ForeignPassportRf(
            **passport_data.model_dump(),
            id=passport_id,
            is_verified=is_verified
        )

    try:
        session.add(passport)
        await session.flush()
    except DatabaseError as error:
        raise foreign_passport_rf_not_specified_exception from error
    return passport.to_schema()


def _update_passport_fields(*, passport, fields: dict):
    for field, value in fields.items():
        if value is not None:
            setattr(passport, field, value)
