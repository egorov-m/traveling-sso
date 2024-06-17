import pytest
import allure

from traveling_sso.database.models import User, Client
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.managers.custom_auth import CustomAuthManager
from traveling_sso.shared.schemas.exceptions import user_not_specified_exception

@allure.title("Successful signin with valid credentials")
@allure.feature("Custom Auth Management")
@allure.description("Verify that signin with valid email and password returns a valid token response")
async def test_signin_success(session: AsyncSession, client: Client):
    auth_manager = CustomAuthManager(session=session, password="password", email=client.user.email, client_id=client.client_id)
    token_response = await auth_manager.signin()
    assert token_response is not None

@allure.title("Fail signin with invalid email")
@allure.feature("Custom Auth Management")
@allure.description("Verify that signin with invalid email raises a user not specified exception")
async def test_signin_invalid_email(user: User, session: AsyncSession, client: Client):
    auth_manager = CustomAuthManager(session=session, password="password", email="tests@mail.com", client_id=client.client_id)
    with pytest.raises(type(user_not_specified_exception)):
        await auth_manager.signin()


@allure.title("Fail signin with invalid password")
@allure.feature("Custom Auth Management")
@allure.description("Verify that signin with invalid password raises a user not specified exception")
async def test_signin_invalid_password(user: User, session: AsyncSession, client: Client):
    auth_manager = CustomAuthManager(session=session, password="pass", email=client.user.email, client_id=client.client_id)
    with pytest.raises(type(user_not_specified_exception)):
        await auth_manager.signin()

@allure.title("Fail signin without client id")
@allure.feature("Custom Auth Management")
@allure.description("Verify that signin without client id raises an assertion error")
async def test_signin_no_client_id(user: User, session: AsyncSession, client: Client):
    auth_manager = CustomAuthManager(session=session, password="password", email=client.user.email, client_id=client.id)
    with pytest.raises(type(user_not_specified_exception)):
        await auth_manager.signin()
