from uuid import uuid4

import allure
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.database.models import Client, TokenSession
from traveling_sso.managers.token import generate_access_token, JWTClaims


@allure.title("Create token session")
@allure.feature("Token Management")
@allure.description("This test verifies that the refresh token session has been correctly created in the database.")
async def test_create_token_session(session: AsyncSession, client: Client):
    from traveling_sso.shared.schemas.protocol import TokenType
    from traveling_sso.managers import create_token_session

    token_type = str(TokenType.Bearer)

    token = await create_token_session(
        session=session,
        user=client.user,
        client=client,
        token_type=token_type
    )

    assert token.refresh_token is not None
    assert token.access_token is not None
    assert token.token_type == token_type
    assert token.expires is not None


@allure.title("Get token session by id — not found.")
@allure.feature("Token Management")
@allure.description("This test verifies if an exception occurs correctly if a non-existent token session is received.")
async def test_get_token_session_by_session_id_not_found(session: AsyncSession):
    from traveling_sso.managers import get_token_session_by_session_id
    from traveling_sso.shared.schemas.exceptions import SsoException
    from traveling_sso.shared.schemas.exceptions.templates import auth_session_not_found_exception

    session_id = str(uuid4())

    with pytest.raises(SsoException) as exc_info:
        await get_token_session_by_session_id(
            session=session,
            session_id=session_id
        )

        error = exc_info.value
        assert error.error_code == auth_session_not_found_exception.error_code
        assert error.http_status_code == auth_session_not_found_exception.http_status_code


@allure.title("Get token session by id.")
@allure.feature("Token Management")
@allure.description("This test verifies if it is correct to get a token session by its session id.")
async def test_get_token_session_by_session_id(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import get_token_session_by_session_id

    output_token = await get_token_session_by_session_id(
            session=session,
            session_id=token_session.id
        )

    assert token_session.__dict__ == output_token.__dict__


@allure.title("Get token session by refresh token — not found.")
@allure.feature("Token Management")
@allure.description("This test verifies if an exception occurs correctly if a non-existent token session is received.")
async def test_get_token_session_by_refresh_token_not_found(session: AsyncSession):
    from traveling_sso.managers import get_token_session_by_refresh_token
    from traveling_sso.shared.schemas.exceptions import SsoException
    from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception

    refresh_token = str(uuid4())

    with pytest.raises(SsoException) as exc_info:
        await get_token_session_by_refresh_token(
            session=session,
            refresh_token=refresh_token
        )

        error = exc_info.value
        assert error.error_code == auth_refresh_token_no_valid_exception.error_code
        assert error.http_status_code == auth_refresh_token_no_valid_exception.http_status_code


@allure.title("Get token session by refresh token.")
@allure.feature("Token Management")
@allure.description("This test verifies if it is correct to get a token session by its refresh token.")
async def test_get_token_session_by_refresh_token(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import get_token_session_by_refresh_token

    output_token = await get_token_session_by_refresh_token(
        session=session,
        refresh_token=token_session.refresh_token
    )

    assert token_session.__dict__ == output_token.__dict__


@allure.title("Get count active session for user.")
@allure.feature("Token Management")
@allure.description("The test verifies the correctness of get the count of active user sessions.")
async def test_get_count_active_token_session_for_user(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import get_count_active_token_session_for_user

    output_count = await get_count_active_token_session_for_user(
        session=session,
        user_id=token_session.user_id
    )

    assert output_count == 1


@allure.title("Revoke all active sessions for user.")
@allure.feature("Token Management")
@allure.description("This test verifies if all active user sessions have been revoked back correctly.")
async def test_revoke_all_active_token_sessions_for_user(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import get_count_active_token_session_for_user
    from traveling_sso.managers import revoke_all_active_token_sessions_for_user

    with allure.step("Check the initial count of active sessions."):
        output_count = await get_count_active_token_session_for_user(
            session=session,
            user_id=token_session.user_id
        )

        assert output_count > 0

    with allure.step("Revocation of all active sessions for user."):
        await revoke_all_active_token_sessions_for_user(
            session=session,
            user_id=token_session.user_id
        )

    with allure.step("Check that all user sessions are revoked."):
        output_count = await get_count_active_token_session_for_user(
            session=session,
            user_id=token_session.user_id
        )

        assert output_count == 0


@allure.title("Get token session for user.")
@allure.feature("Token Management")
@allure.description("This test verifies if it is correct to retrieve a list of sessions for a user.")
async def test_get_token_sessions_by_user_id(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import get_token_sessions_by_user_id
    from traveling_sso.shared.schemas.protocol import TokenSessionSchema

    output_sessions = await get_token_sessions_by_user_id(
        session=session,
        user_id=token_session.user_id,
        client_id=token_session.client_id
    )

    assert len(output_sessions) == 1

    output_session: TokenSessionSchema = output_sessions[0]

    assert output_session.session_id == token_session.id
    assert output_session.issued_at == token_session.issued_at
    assert output_session.expires_at == token_session.issued_at + token_session.expires_in


@allure.title("Revoke token session.")
@allure.feature("Token Management")
@allure.description("This test verifies the correctness of the session revoke.")
async def test_revoke_token_session(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import revoke_token_session
    from traveling_sso.managers import get_user_by_identifier
    from traveling_sso.managers import get_token_session_by_refresh_token
    from traveling_sso.shared.schemas.exceptions import SsoException
    from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception

    refresh_token = token_session.refresh_token

    user = await get_user_by_identifier(
        session=session,
        identifier=token_session.user_id
    )

    with allure.step("Revoking off the session."):
        assert await revoke_token_session(
            session=session,
            user=user,
            session_id=token_session.id
        )

    with allure.step("Checking that the session is revoked."):
        with pytest.raises(SsoException) as exc_info:
            await get_token_session_by_refresh_token(
                session=session,
                refresh_token=refresh_token
            )

            error = exc_info.value
            assert error.error_code == auth_refresh_token_no_valid_exception.error_code
            assert error.http_status_code == auth_refresh_token_no_valid_exception.http_status_code


@allure.title("Generate and validate access token.")
@allure.feature("Token Management")
@allure.description("This test verifies the correctness of access token generation and validation.")
async def test_generate_and_validate_access_token(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import (
        get_user_by_identifier,
        validate_access_token,
        split_access_token,
        get_client_by_client_id
    )

    user = await get_user_by_identifier(
        session=session,
        identifier=token_session.user_id
    )

    client = await get_client_by_client_id(
        session=session,
        client_id=token_session.client_id
    )

    with allure.step("Generate an access token."):
        output_token = generate_access_token(
            user_id=str(user.id),
            user_role=user.role,
            client_id=token_session.client_id,
            secret=client.client_private_secret,
            session_id=str(token_session.id),
        )

        assert isinstance(output_token, str)

    with allure.step("Access token validation."):
        client_id, jwt_token = split_access_token(output_token)

        assert client_id == client.client_id

        jwt_claims_output = validate_access_token(
            client=client,
            jwt_token=jwt_token
        )

        assert isinstance(jwt_claims_output, JWTClaims)


@allure.title("Update refresh token.")
@allure.feature("Token Management")
@allure.description("This test verifies if the token refresh is correct.")
async def test_update_refresh_token(session: AsyncSession, token_session: TokenSession):
    from traveling_sso.managers import (
        get_user_by_id,
        validate_access_token,
        split_access_token,
        get_client_by_client_id,
        update_refresh_token
    )

    from traveling_sso.managers import get_token_session_by_refresh_token
    from traveling_sso.shared.schemas.exceptions import SsoException
    from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception

    user = await get_user_by_id(
        session=session,
        user_id=token_session.user_id
    )

    client = await get_client_by_client_id(
        session=session,
        client_id=token_session.client_id
    )

    orig_refresh_token = token_session.refresh_token

    with allure.step("Updating refresh token."):
        response_token_schema = await update_refresh_token(
            session=session,
            token=token_session,
            client=client,
            user=user
        )

    with allure.step("Let's verify that the token was actually changed."):
        assert response_token_schema.refresh_token != orig_refresh_token

        with pytest.raises(SsoException) as exc_info:
            await get_token_session_by_refresh_token(
                session=session,
                refresh_token=orig_refresh_token
            )

            error = exc_info.value
            assert error.error_code == auth_refresh_token_no_valid_exception.error_code
            assert error.http_status_code == auth_refresh_token_no_valid_exception.http_status_code

        output_token = await get_token_session_by_refresh_token(
            session=session,
            refresh_token=str(response_token_schema.refresh_token)
        )
        assert token_session.__dict__ == output_token.__dict__

        access_token = response_token_schema.access_token

    with allure.step("New access token validation."):
        client_id, jwt_token = split_access_token(access_token)

        assert client_id == client.client_id

        jwt_claims_output = validate_access_token(
            client=client,
            jwt_token=jwt_token
        )

        assert isinstance(jwt_claims_output, JWTClaims)


@allure.title("Revocation of sessions by limit.")
@allure.feature("Token Management")
@allure.description("This test verifies that all sessions are correctly revoked when the count limit is exceeded.")
async def test_session_revocation_when_count_exceeds_limit_for_user(session: AsyncSession, client: Client):
    from traveling_sso.managers import get_count_active_token_session_for_user
    from traveling_sso.shared.schemas.protocol import TokenType
    from traveling_sso.managers import create_token_session
    from traveling_sso.config import settings

    count = settings.ACTIVE_REFRESH_TOKEN_MAX_COUNT + 1

    for _ in range(count):
        token_type = str(TokenType.Bearer)

        await create_token_session(
            session=session,
            user=client.user,
            client=client,
            token_type=token_type
        )

    output_count = await get_count_active_token_session_for_user(
        session=session,
        user_id=client.user_id
    )

    assert output_count == 1
