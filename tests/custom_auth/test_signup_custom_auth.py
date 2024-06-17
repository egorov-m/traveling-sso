import allure
import pytest
from uuid_extensions import uuid7
from sqlalchemy.ext.asyncio import AsyncSession
from traveling_sso.database.models import Client, User
from traveling_sso.managers.custom_auth import CustomAuthManager
from traveling_sso.shared.schemas.exceptions import user_conflict_exception


@allure.title("Successful signup with client ID")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that a user can signup successfully with a client ID.")
async def test_signup_with_client_id(session: AsyncSession, client: Client, user: User):
    auth_manager = CustomAuthManager(session=session, password=uuid7().hex, email=f"test-{str(uuid7())}@example.com", client_id=client.client_id)
    token_response = await auth_manager.signup()
    assert token_response is not None

@allure.title("Successful signup without client ID")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that a user can signup successfully without a client ID.")
async def test_signup_without_client_id(session: AsyncSession,user: User, client: Client):
    auth_manager = CustomAuthManager(session=session, password=uuid7().hex, email=f"test-{str(uuid7())}@example.com",
                                     client_id=client.id)
    with pytest.raises(type(user_conflict_exception)):
        await auth_manager.signup()


@allure.title("Email address already in use")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that an error is raised when trying to signup with an email address that is already in use.")
async def test_signup_email_address_in_use(session: AsyncSession, user: User, client: Client):
    auth_manager = CustomAuthManager(session=session, password=uuid7().hex, email=client.user.email,
                                     client_id=client.id)
    with pytest.raises(type(user_conflict_exception)):
        await auth_manager.signup()


