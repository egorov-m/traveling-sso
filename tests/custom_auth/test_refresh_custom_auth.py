from uuid import uuid4

import allure
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from traveling_sso.database.models import TokenSession, Client, User
from traveling_sso.managers import create_token_session
from traveling_sso.managers.custom_auth import CustomAuthManager
from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception, \
    client_not_found_exception
from traveling_sso.shared.schemas.protocol import TokenType

@allure.title("Refresh token is valid")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that a valid refresh token returns a new token.")
async def test_refresh_token_valid(session: AsyncSession, token_session: TokenSession, client: Client, user: User):
    async with session:
        token = await create_token_session(session=session, user=user, client=client, token_type=str(TokenType.Bearer))
        refreshed_token = await CustomAuthManager.refresh(session=session, refresh_token=token.refresh_token)
    assert refreshed_token is not None

@allure.title("Refresh token is invalid")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that an invalid refresh token raises an exception.")
async def test_refresh_token_invalid(session: AsyncSession, client: Client, user: User, token_session: TokenSession):
    async with session:
        invalid_refresh_token = str(uuid4())
        with pytest.raises(type(auth_refresh_token_no_valid_exception)):
            await CustomAuthManager.refresh(session=session, refresh_token=invalid_refresh_token)


@allure.title("Client not found for refresh token")
@allure.feature("Custom Auth Management")
@allure.description("This test verifies that a refresh token with a non-existent client raises an exception.")
async def test_refresh_token_client_not_found(session: AsyncSession, client: Client, token_session: TokenSession):
    async with session:
        await session.delete(client)
        with pytest.raises(type(client_not_found_exception)):
            await CustomAuthManager.refresh(session=session, refresh_token=token_session.refresh_token)


