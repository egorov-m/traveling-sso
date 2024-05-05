from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.exceptions import (
    user_not_found_exception,
    user_not_specified_exception
)
from traveling_sso.shared.schemas.protocol import (
    UserSchema,
    InternalCreateUserResponseSchema
)
from ..database.models import User


async def get_user_by_identifier(*, session: AsyncSession, identifier) -> UserSchema:
    user = await _get_user_by_identifier(session=session, identifier=str(identifier))
    if user is None:
        raise user_not_found_exception

    return user.to_schema()


async def create_or_update_user(*, session: AsyncSession, user_data: InternalCreateUserResponseSchema) -> User:
    user = await _get_user_by_identifier(session=session, identifier=str(user_data.id))
    if user is None:
        user = User(**user_data.model_dump())
    else:
        update_data = user_data.model_dump()
        update_data.pop("id", None)
        _update_user_fields(user=user, fields=update_data)

    try:
        session.add(user)
        await session.flush()
    except DatabaseError as error:
        raise user_not_specified_exception from error

    return user


async def _get_user_by_identifier(*, session: AsyncSession, identifier) -> User | None:
    identifier = str(identifier)
    query = select(User).where(
        or_(
            User.id == str(identifier),
            User.email == str(identifier),
            User.username == str(identifier)
        )
    )
    user = (await session.execute(query)).scalar()

    return user


def _update_user_fields(*, user: User, fields: dict):
    for field, value in fields.items():
        if value is not None:
            setattr(user, field, value)
