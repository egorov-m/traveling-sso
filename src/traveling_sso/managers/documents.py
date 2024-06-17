from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import (
    PassportRfSchema,
    ForeignPassportRfSchema,
    CreatePassportRfResponseSchema,
    CreateForeignPassportRfResponseSchema,
    UpdatePassportRfResponseSchema,
    UpdateForeignPassportRfResponseSchema
)
from traveling_sso.shared.schemas.exceptions import (
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception,
    passport_rf_already_exists_exception
)
from .user import add_passport_rf, add_foreign_passport_rf
from ..database.models import PassportRf, User, ForeignPassportRf
from ..shared.schemas.exceptions.templates import foreign_passport_rf_already_exists_exception


async def get_all_documents_by_user_id(*, session: AsyncSession, user_id) -> dict:
    passport = await _get_passport_rf_by_user_id(session, user_id)
    passport_foreign = await _get_foreign_passport_rf_by_user_id(session, user_id)

    res = {"passport_rf": None, "foreign_passport_rf": None}
    if passport is not None:
        res["passport_rf"] = passport.to_schema()
    if passport_foreign is not None:
        res["foreign_passport_rf"] = passport_foreign.to_schema()
    return res


async def get_passport_rf_by_user_id(*, session: AsyncSession, user_id) -> PassportRfSchema | None:
    passport = await _get_passport_rf_by_user_id(session, user_id)

    if passport is not None:
        return passport.to_schema()


async def _get_passport_rf_by_user_id(session: AsyncSession, user_id):
    query = (select(PassportRf)
             .join(User, User.passport_rf_id == PassportRf.id)
             .where(User.id == str(user_id)))
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
             .join(User, User.foreign_passport_rf_id == ForeignPassportRf.id)
             .where(User.id == str(user_id)))
    passport = (await session.execute(query)).scalar()

    return passport


async def _get_foreign_passport_rf_by_id(session: AsyncSession, passport_id):
    query = select(ForeignPassportRf).where(ForeignPassportRf.id == passport_id)
    passport = (await session.execute(query)).scalar()

    return passport


async def create_passport_rf_new(
        *,
        session: AsyncSession,
        passport_data: CreatePassportRfResponseSchema | UpdatePassportRfResponseSchema,
        user_id: str | None = None,
) -> PassportRfSchema:
    passport = await _get_passport_rf_by_user_id(session, user_id)
    if passport is not None:
        raise passport_rf_already_exists_exception
    passport_id = str(uuid4())
    passport = PassportRf(
        **passport_data.model_dump(),
        id=passport_id,
        is_verified=True
    )
    session.add(passport)
    await add_passport_rf(session=session, passport=passport, user_id=user_id)
    return passport.to_schema()


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
            _update_passport_fields(passport=passport, fields=passport_data.model_dump(exclude_unset=True))
    if passport is None:
        passport_id = passport_id or str(uuid4())
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


async def create_foreign_passport_rf_new(
        *,
        session: AsyncSession,
        passport_data: CreateForeignPassportRfResponseSchema,
        user_id: str | None = None
) -> ForeignPassportRfSchema:
    passport = await get_foreign_passport_rf_by_user_id(session=session, user_id=user_id)
    if passport is not None:
        raise foreign_passport_rf_already_exists_exception
    passport_id = str(uuid4())
    passport = ForeignPassportRf(
        **passport_data.model_dump(),
        id=passport_id,
        is_verified=True
    )
    session.add(passport)
    await add_foreign_passport_rf(session=session, passport=passport, user_id=user_id)
    return passport.to_schema()


async def create_or_update_foreign_passport_rf(
        *,
        session: AsyncSession,
        passport_data: CreateForeignPassportRfResponseSchema | UpdateForeignPassportRfResponseSchema,
        passport_id: str | None = None,
        user_id: str | None = None,
        is_verified: bool = False
) -> ForeignPassportRfSchema:
    assert passport_id is None or user_id is None, "Use one of the identifiers for the search."

    passport = None
    if passport_id is not None or user_id is not None:
        if passport_id is not None:
            passport = await _get_foreign_passport_rf_by_id(session, passport_id)
        else:
            passport = await _get_foreign_passport_rf_by_user_id(session, user_id)
        if passport is not None:
            _update_passport_fields(passport=passport, fields=passport_data.model_dump())
    if passport is None:
        passport_id = passport_id or str(uuid4())
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
        if value is not None and hasattr(passport, field):
            setattr(passport, field, value)


async def update_passport_rf(
        *,
        session: AsyncSession,
        user_id: str,
        passport_data: UpdatePassportRfResponseSchema
) -> PassportRfSchema:
    passport = await _get_passport_rf_by_user_id(session, user_id)
    if not passport:
        raise passport_rf_not_specified_exception

    _update_passport_fields(passport=passport, fields=passport_data.model_dump())

    try:
        session.add(passport)
        await session.flush()
    except DatabaseError as error:
        raise passport_rf_not_specified_exception from error
    return passport.to_schema()


async def update_foreign_passport_rf(
        *,
        session: AsyncSession,
        user_id: str,
        passport_data: UpdateForeignPassportRfResponseSchema
) -> ForeignPassportRfSchema:
    passport = await _get_foreign_passport_rf_by_user_id(session, user_id)
    if not passport:
        raise foreign_passport_rf_not_specified_exception

    _update_passport_fields(passport=passport, fields=passport_data.model_dump())

    try:
        session.add(passport)
        await session.flush()
    except DatabaseError as error:
        raise foreign_passport_rf_not_specified_exception from error
    return passport.to_schema()
