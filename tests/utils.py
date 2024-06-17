from os import environ

from data import TokenData, SessionData
from traveling_sso.config import settings
from traveling_sso.shared.schemas.protocol import TokenType


def assert_status_code(resp, status_code, status_code_debug):
    if environ.get("DEBUG", "false").lower() == "true":
        assert resp.status_code == status_code_debug
    else:
        assert resp.status_code == status_code


def assert_error_code(resp, error_code):
    data = resp.json()
    assert data.get("errors")[0].get("error_code") == error_code


def validate_token_schema(resp) -> TokenData:
    data = resp.json()
    assert isinstance(data.get("access_token"), str)
    assert data.get("token_type") == TokenType.Bearer
    assert isinstance(data.get("expires"), int)

    if settings.IS_REFRESH_TOKEN_VIA_COOKIE:
        refresh_token = resp.cookies.get("sso_refresh_token")
        assert isinstance(refresh_token, str)
    else:
        refresh_token = data.get("refresh_token")
        assert isinstance(refresh_token, str)

    return TokenData(
        access_token=data.get("access_token"),
        refresh_token=refresh_token,
        token_type=data.get("token_type"),
        expires=data.get("expires")
    )


def validate_sessions_list(resp) -> list[SessionData]:
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0

    return [
        SessionData(
            session_id=item.get("session_id"),
            issued_at=item.get("issued_at"),
            expires_at=item.get("expires_at"),
            is_current=item.get("is_current")
        ) for item in data]
