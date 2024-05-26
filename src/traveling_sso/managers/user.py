from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.exceptions import (
    user_not_found_exception,
    user_not_specified_exception,
    user_conflict_exception
)
from traveling_sso.shared.schemas.protocol import (
    UserSchema,
    InternalCreateUserRequestSchema,
    UpdateUserInfoRequestSchema
)
from ..database.models import User
from ..database.utils import is_uuid


async def get_user_by_id(*, session: AsyncSession, user_id) -> User:
    user = await session.get(User, str(user_id))
    if user is None:
        raise user_not_found_exception

    return user


async def get_user_by_identifier(*, session: AsyncSession, identifier) -> UserSchema:
    user = await _get_user_by_identifier(session=session, identifier=str(identifier))
    if user is None:
        raise user_not_found_exception

    return user.to_schema()


async def create_or_update_user(*, session: AsyncSession, user_data: InternalCreateUserRequestSchema) -> User:
    user = None
    if user_data.id is not None:
        user = await _get_user_by_identifier(session=session, identifier=str(user_data.id))
    if user is None:
        user = User(**user_data.model_dump())
    else:
        update_data = user_data.model_dump()
        update_data.pop("id", None)
        password = update_data.pop("password", None)
        if password is not None:
            update_data["password_hash"] = User.get_password_hash(password)
        _update_user_fields(user=user, fields=update_data)

    try:
        session.add(user)
        await session.flush()
    except DatabaseError as error:
        raise user_not_specified_exception from error

    return user


async def update_user(*, session: AsyncSession, user_id,  user_data: UpdateUserInfoRequestSchema) -> UserSchema:
    user = await get_user_by_id(session=session, user_id=user_id)

    if user_data.email is not None and user_data.email != user.email:
        user.email = user_data.email
    if user_data.username is not None and user_data.username != user.username:
        user.username = user_data.username
    if user_data.password is not None:
        user.password_hash = User.get_password_hash(user_data.password)

    try:
        session.add(user)
        await session.flush()
    except DatabaseError as error:
        raise user_conflict_exception from error

    return user.to_schema()


async def _get_user_by_identifier(*, session: AsyncSession, identifier) -> User | None:
    identifier = str(identifier)
    clauses = [User.email == str(identifier), User.username == str(identifier)]
    if is_uuid(identifier):
        clauses.append(User.id == str(identifier))
    query = select(User).where(or_(*clauses))
    user = (await session.execute(query)).scalar()

    return user


def _update_user_fields(*, user: User, fields: dict):
    for field, value in fields.items():
        if value is not None:
            setattr(user, field, value)
