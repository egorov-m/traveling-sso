from uuid import uuid4

import allure
from authlib.common.security import generate_token
from httpx import AsyncClient

from sys import path
path.append("../../data.py")
path.append("../../utils.py")

from data import TokenData, SessionData
from utils import assert_status_code, assert_error_code, validate_token_schema
from traveling_sso.config import settings
from traveling_sso.shared.schemas.exceptions import SsoErrorCode


BASE_PATH = "/api/v1/auth"


@allure.title("SignUp with no exist client.")
@allure.feature("Auth API")
async def test_signup_no_exist_client(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signup?client_id={generate_token(48)}",
        json={
            "email": f"{uuid4().hex}@example.com",
            "password": str(uuid4())
        }
    )
    assert_status_code(resp, 400, 404)
    assert_error_code(resp, SsoErrorCode.CLIENT_NOT_FOUND)


@allure.title("SignUp user conflict.")
@allure.feature("Auth API")
async def test_signup_user_conflict(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signup?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "email": settings.ROOT_ADMIN_USER["email"],
            "password": str(uuid4())
        }
    )
    assert_status_code(resp, 400, 409)
    assert_error_code(resp, SsoErrorCode.USER_NOT_SPECIFIED)


@allure.title("SignUp with getting token.")
@allure.feature("Auth API")
async def test_signup_with_getting_token(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signup?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "email": f"{uuid4().hex}@example.com",
            "password": str(uuid4())
        }
    )
    assert resp.status_code == 200
    validate_token_schema(resp)


@allure.title("SignUp.")
@allure.feature("Auth API")
async def test_signup(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signup",
        json={
            "email": f"{uuid4().hex}@example.com",
            "password": str(uuid4())
        }
    )
    assert resp.status_code == 200
    assert resp.text == "null"


@allure.title("SignIn with no exist client.")
@allure.feature("Auth API")
async def test_signin_no_exist_client(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signin?client_id={generate_token(48)}",
        json={
            "login": settings.ROOT_ADMIN_USER["email"],
            "password": settings.ROOT_ADMIN_USER["password"]
        }
    )
    assert_status_code(resp, 400, 404)
    assert_error_code(resp, SsoErrorCode.CLIENT_NOT_FOUND)


@allure.title("SignIn user not specified.")
@allure.feature("Auth API")
async def test_signin_not_specified(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signin?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "login": f"{uuid4().hex}@example.com",
            "password": str(uuid4())
        }
    )
    assert_status_code(resp, 400, 400)
    assert_error_code(resp, SsoErrorCode.USER_NOT_SPECIFIED)


@allure.title("SignIn.")
@allure.feature("Auth API")
async def test_signin(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/signin?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "login": settings.ROOT_ADMIN_USER["email"],
            "password": settings.ROOT_ADMIN_USER["password"]
        }
    )
    assert resp.status_code == 200
    validate_token_schema(resp)


@allure.title("Logout unauthorized.")
@allure.feature("Auth API")
async def test_logout_unauthorized(sso_service: AsyncClient):
    resp = await sso_service.post(f"{BASE_PATH}/logout")
    assert_status_code(resp, 400, 401)
    assert_error_code(resp, SsoErrorCode.AUTH_UNAUTHORIZED)


@allure.title("Logout no valid token.")
@allure.feature("Auth API")
async def test_logout_no_valid_token(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/logout",
        headers={
            "Authorization": f"Bearer {uuid4().hex}"
        }
    )
    assert_status_code(resp, 400, 403)
    assert_error_code(resp, SsoErrorCode.AUTH_ACCESS_TOKEN_NO_VALID)


@allure.title("Logout.")
@allure.feature("Auth API")
async def test_logout(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/logout",
        headers={
            "Authorization": f"Bearer {sso_admin_token.access_token}"
        }
    )
    assert resp.status_code == 200
    assert resp.text == "true"


@allure.title("Refresh session without token.")
@allure.feature("Auth API")
async def test_session_refresh_without_token(sso_service: AsyncClient):
    resp = await sso_service.post(f"{BASE_PATH}/session/refresh")
    assert_status_code(resp, 400, 403)
    assert_error_code(resp, SsoErrorCode.AUTH_REFRESH_TOKEN_NO_VALID)


@allure.title("Refresh session no valid tokens (cookie, header).")
@allure.feature("Auth API")
async def test_session_refresh_no_valid_tokens(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/refresh",
        headers={
            "x-sso-refresh-token": str(uuid4())
        },
        cookies={
            "sso_refresh_token": str(uuid4())
        }
    )
    assert_status_code(resp, 400, 403)
    assert_error_code(resp, SsoErrorCode.AUTH_REFRESH_TOKEN_NO_VALID)


@allure.title("Refresh session no valid token in cookie.")
@allure.feature("Auth API")
async def test_session_refresh_no_valid_cookie_token(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/refresh",
        headers={
            "x-sso-refresh-token": sso_admin_token.refresh_token
        },
        cookies={
            "sso_refresh_token": str(uuid4())
        }
    )
    assert_status_code(resp, 400, 403)
    assert_error_code(resp, SsoErrorCode.AUTH_REFRESH_TOKEN_NO_VALID)


@allure.title("Refresh session no valid token in header.")
@allure.feature("Auth API")
async def test_session_refresh_no_valid_header_token(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/refresh",
        headers={
            "x-sso-refresh-token": str(uuid4())
        },
        cookies={
            "sso_refresh_token": sso_admin_token.refresh_token
        }
    )
    assert resp.status_code == 200
    validate_token_schema(resp)


@allure.title("Refresh session token in cookie.")
@allure.feature("Auth API")
async def test_session_refresh_valid_cookie_token(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/refresh",
        cookies={
            "sso_refresh_token": sso_admin_token.refresh_token
        }
    )
    assert resp.status_code == 200
    validate_token_schema(resp)


@allure.title("Refresh session token in header.")
@allure.feature("Auth API")
async def test_session_refresh_valid_header_token(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/refresh",
        headers={
            "x-sso-refresh-token": sso_admin_token.refresh_token
        }
    )
    assert resp.status_code == 200
    validate_token_schema(resp)


@allure.title("Revoke session no valid access token.")
@allure.feature("Auth API")
async def test_session_revoke_no_valid_access_token(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/revoke",
        headers={
            "Authorization": f"Bearer {uuid4()}"
        }
    )
    assert_status_code(resp, 400, 403)
    assert_error_code(resp, SsoErrorCode.AUTH_ACCESS_TOKEN_NO_VALID)


@allure.title("Revoke session unauthorized.")
@allure.feature("Auth API")
async def test_session_revoke_unauthorized(sso_service: AsyncClient):
    resp = await sso_service.post(f"{BASE_PATH}/session/revoke")
    assert_status_code(resp, 400, 401)
    assert_error_code(resp, SsoErrorCode.AUTH_UNAUTHORIZED)


@allure.title("Revoke session no exist session.")
@allure.feature("Auth API")
async def test_session_revoke_no_exist_session_id(sso_service: AsyncClient, sso_admin_token: TokenData):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/revoke?session_id={uuid4()}",
        headers={
            "Authorization": f"Bearer {sso_admin_token.access_token}"
        }
    )
    assert_status_code(resp, 400, 404)
    assert_error_code(resp, SsoErrorCode.AUTH_SESSION_NOT_FOUND)


@allure.title("Revoke session alive session user.")
@allure.feature("Auth API")
async def test_session_revoke_alien_session_user(
        sso_service: AsyncClient,
        sso_get_admin_sessions: list[SessionData],
        sso_token: TokenData
):
    resp = await sso_service.post(
        f"{BASE_PATH}/session/revoke?session_id={sso_get_admin_sessions[0].session_id}",
        headers={
            "Authorization": f"Bearer {sso_token.access_token}"
        }
    )
    assert_status_code(resp, 400, 404)
    assert_error_code(resp, SsoErrorCode.AUTH_SESSION_NOT_FOUND)


async def _test_session_revoke_success(_resp):
    resp = await _resp()
    assert resp.status_code == 200
    assert resp.text == "true"
    resp = await _resp()  # verifying that the session was indeed revoked
    assert_status_code(resp, 400, 404)
    assert_error_code(resp, SsoErrorCode.AUTH_SESSION_NOT_FOUND)


@allure.title("Revoke session alive session admin user.")
@allure.feature("Auth API")
async def test_session_revoke_alien_session_admin_user(
        sso_service: AsyncClient,
        sso_get_sessions: list[SessionData],
        sso_admin_token: TokenData
):
    async def _resp():
        return await sso_service.post(
            f"{BASE_PATH}/session/revoke?session_id={sso_get_sessions[0].session_id}",
            headers={
                "Authorization": f"Bearer {sso_admin_token.access_token}"
            }
        )

    await _test_session_revoke_success(_resp)


@allure.title("Revoke session by id.")
@allure.feature("Auth API")
async def test_session_revoke_by_id(
        sso_service: AsyncClient,
        sso_get_admin_sessions: list[SessionData],
        sso_admin_token: TokenData
):
    async def _resp():
        return await sso_service.post(
            f"{BASE_PATH}/session/revoke?session_id={sso_get_admin_sessions[0].session_id}",
            headers={
                "Authorization": f"Bearer {sso_admin_token.access_token}"
            }
        )
    await _test_session_revoke_success(_resp)


@allure.title("Revoke current session.")
@allure.feature("Auth API")
async def test_session_revoke_current_session(sso_service: AsyncClient, sso_admin_token: TokenData):
    async def _resp():
        return await sso_service.post(
            f"{BASE_PATH}/session/revoke",
            headers={
                "Authorization": f"Bearer {sso_admin_token.access_token}"
            }
        )
    await _test_session_revoke_success(_resp)
