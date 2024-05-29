import allure
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from traveling_sso.database.models import User


@allure.title("Get User By ID")
@allure.feature("User Management")
@allure.description("This test verifies the functionality of retrieving a user by ID from database.")
async def test_get_user_by_id(session: AsyncSession, user: User):
    from traveling_sso.managers.user import get_user_by_id

    user_by_id = await get_user_by_id(
        session=session,
        user_id=user.id
    )
    assert user_by_id.id == user.id


@allure.title("Get User By Identifier")
@allure.feature("User Management")
@allure.description(
    "This test validates the functionality of retrieving a user by different identifiers such as ID, "
    "email, and username from database."
)
async def test_get_user_by_identifier(session: AsyncSession, user: User):
    from traveling_sso.managers import get_user_by_identifier

    with allure.step("Check by id."):
        user_by_id = await get_user_by_identifier(
            session=session,
            identifier=user.id
        )
        assert str(user_by_id.id) == user.id
    with allure.step("Check by email."):
        user_by_email = await get_user_by_identifier(
            session=session,
            identifier=user.email
        )
        assert str(user_by_email.email) == user.email
    with allure.step("Check by username."):
        user_by_username = await get_user_by_identifier(
            session=session,
            identifier=user.username
        )
        assert str(user_by_username.username) == user.username


@allure.title("Create User")
@allure.feature("User Management")
@allure.description("This test is to verify that a new user has been created correctly in the database.")
async def test_create_user(session: AsyncSession):
    from traveling_sso.managers import create_or_update_user
    from traveling_sso.shared.schemas.protocol import UserRoleType, InternalCreateUserRequestSchema

    user_schema = InternalCreateUserRequestSchema(
        id=uuid7(),
        role=UserRoleType.user,
        email=f"{uuid7()}@example.com",
        password=uuid7().hex,
        username=uuid7().hex
    )
    user = await create_or_update_user(
        session=session,
        user_data=user_schema
    )

    _assert_fields(user, user_schema)


@allure.title("Internal update User")
@allure.feature("User Management")
@allure.description("This test will verify that the user (internal data) update is correct in the database.")
async def test_internal_update_user(session: AsyncSession, user: User):
    from traveling_sso.managers import create_or_update_user
    from traveling_sso.shared.schemas.protocol import InternalCreateUserRequestSchema

    user_schema = InternalCreateUserRequestSchema(
        id=user.id,
        role=user.role,
        email=f"{uuid7()}@example.com",
        password=uuid7().hex,
        username=uuid7().hex
    )
    user = await create_or_update_user(
        session=session,
        user_data=user_schema
    )
    _assert_fields(user, user_schema)


@allure.title("Update User")
@allure.feature("User Management")
@allure.description("This test will verify that the user info update is correct in the database.")
async def test_update_user(session: AsyncSession, user: User):
    from traveling_sso.managers import update_user, get_user_by_id
    from traveling_sso.shared.schemas.protocol import UpdateUserInfoRequestSchema

    user_data = UpdateUserInfoRequestSchema(
        email=f"{uuid7()}@example.com",
        username=uuid7().hex,
        password=uuid7().hex
    )
    user_schema = await update_user(
        session=session,
        user_id=user.id,
        user_data=user_data
    )
    user = await get_user_by_id(
        session=session,
        user_id=user.id
    )
    assert user_schema.email == user_data.email
    assert user_schema.username == user_data.username
    assert user.password_hash == User.get_password_hash(user_data.password)


@allure.title("Update User with conflict info.")
@allure.feature("User Management")
@allure.description("Test checking for conflict occurrence when updating user info.")
async def test_update_user_with_conflict_info(session: AsyncSession, user: User):
    from traveling_sso.managers import create_or_update_user, update_user
    from traveling_sso.shared.schemas.exceptions import SsoException
    from traveling_sso.shared.schemas.protocol import InternalCreateUserRequestSchema, UpdateUserInfoRequestSchema

    with allure.step("Create a user for the conflict."):
        conflict_user_schema = InternalCreateUserRequestSchema(
            id=uuid7(),
            role=user.role,
            email=f"{uuid7()}@example.com",
            password=uuid7().hex,
            username=uuid7().hex
        )
        conflict_user = await create_or_update_user(
            session=session,
            user_data=conflict_user_schema
        )
    with allure.step("Performing an update with a conflict."):
        user_data = UpdateUserInfoRequestSchema(
            email=conflict_user_schema.email,
            username=conflict_user_schema.username,
            password=uuid7().hex
        )
        with pytest.raises(SsoException):
            await update_user(
                session=session,
                user_id=user.id,
                user_data=user_data
            )


def _assert_fields(u1, u2):
    assert str(u1.id) == str(u2.id)
    assert u1.role == str(u2.role)
    assert u1.email == u2.email
    assert u1.username == u2.username
    assert u1.check_password(u2.password)
