from fastapi import Depends, Security
from fastapi.security import HTTPBearer, APIKeyCookie, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.config import settings
from traveling_sso.database.deps import get_db
from traveling_sso.managers import get_client_by_client_id, get_user_by_identifier
from traveling_sso.managers.token import validate_access_token, split_access_token
from traveling_sso.shared.schemas.exceptions import SsoException
from traveling_sso.shared.schemas.exceptions.templates import (
    auth_unauthorized_exception,
    auth_access_denied_exception,
    auth_access_token_no_valid_exception
)
from traveling_sso.shared.schemas.protocol import UserRoleType


sso_access_token = HTTPBearer(
    scheme_name="Access token",
    description="Access token in jwt format.",
    auto_error=False
)
sso_refresh_token = APIKeyCookie(
    scheme_name="Refresh token",
    name=settings.REFRESH_TOKEN_COOKIE_NAME,
    description="Refresh token to update the access token in UUID format.",
    auto_error=False
)


class AuthSsoUser:

    def __init__(self, required_role: UserRoleType = UserRoleType.user):
        self.required_role = required_role

    async def __call__(
            self,
            access_token: HTTPAuthorizationCredentials = Security(sso_access_token),
            session: AsyncSession = Depends(get_db)
    ):
        if access_token:
            client_id, jwt_token = split_access_token(access_token.credentials)
            try:
                client = await get_client_by_client_id(
                    session=session,
                    client_id=client_id
                )
            except SsoException as error:
                raise auth_access_token_no_valid_exception from error

            decode_token: dict = validate_access_token(
                client=client,
                jwt_token=jwt_token
            )
            user_id = decode_token["sub"]

            user_schema = await get_user_by_identifier(
                session=session,
                identifier=user_id
            )

            if self.required_role == user_schema.role or user_schema.role == UserRoleType.admin:
                return user_schema
            else:
                raise auth_access_denied_exception

        raise auth_unauthorized_exception
