from uuid import uuid4

from authlib.jose import RSAKey, JWTClaims as _JWTClaims, JsonWebToken
from authlib.jose.errors import JoseError
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import TokenResponseSchema
from ..config import settings
from ..database.models import Client, TokenSession, User
from ..database.utils import utcnow
from ..shared.schemas.exceptions.templates import auth_access_token_no_valid_exception

__algorithm__ = "RS512"
__separator__ = ":"
jwt = JsonWebToken([__algorithm__])


class JWTClaims(_JWTClaims):

    _sso_options = {
        "iss": {"value": settings.SSO_ISSUERS},
        "sub": {"essential": True},
        "aud": {"essential": True},
        "exp": {"value": settings.ACCESS_TOKEN_EXPIRES_IN},
        "ndf": {"essential": True},
        "iat": {"essential": True},
        "jti": {"essential": True},

        # custom claims
        "user_role": {"essential": True}
    }

    def __init__(self, payload, header, options=None, params=None):
        options = options or {}
        super().__init__(
            payload,
            header,
            options={
                **self._sso_options,
                **options
            },
            params=params
        )

    @classmethod
    def factory_claims(cls, user_id, client_id, user_role) -> "JWTClaims":
        now = int(utcnow().timestamp())
        return cls(
            payload={
                "iss": settings.SSO_ISSUERS,
                "sub": user_id,
                "aud": client_id,
                "exp": now + settings.ACCESS_TOKEN_EXPIRES_IN,
                "ndf": now,
                "iat": now,
                "jti": str(uuid4()),
                "user_role": user_role
            },
            header={
                "alg": __algorithm__,
                "typ": "JWT"
            }
        )


async def create_token_session(
        *,
        session: AsyncSession,
        user: User,
        client: Client,
        token_type: str,
        expires_in: int = settings.REFRESH_TOKEN_EXPIRES_IN
) -> TokenResponseSchema:
    token = TokenSession(
        client_id=client.client_id,
        token_type=token_type,
        refresh_token=str(uuid4()),
        expires_in=expires_in,
        user=user
    )
    session.add(token)
    await session.flush()
    return token.to_response_schema(access_token=generate_access_token(
        str(user.id), user.role, client.client_id, client.client_private_secret
    ))


def generate_access_token(user_id, user_role, client_id, secret):
    claims = JWTClaims.factory_claims(user_id, client_id, user_role)
    token = jwt.encode(claims.header, claims, RSAKey.import_key(secret).get_private_key())

    return f"{client_id}{__separator__}{token.decode('utf-8')}"


def validate_access_token(
        *,
        client: Client,
        jwt_token: str,
):
    assert len(jwt_token.split(__separator__)) == 1, "Only the jwt token itself needs to be passed for validation."

    try:
        decode_token = jwt.decode(
            jwt_token,
            client.client_private_secret,
            claims_cls=JWTClaims
        )
        decode_token.validate(int(utcnow().timestamp()))
    except JoseError as error:
        raise auth_access_token_no_valid_exception from error

    if decode_token["aud"] != client.client_id:
        raise auth_access_token_no_valid_exception

    return decode_token


def split_access_token(access_token: str) -> tuple[str, str]:
    """
        Access token split in the format: <client_id>:<jwt_token>
        :param access_token:
        :return: tuple[<client_id>, <jwt_token>]
    """
    s = access_token.split(__separator__)
    if len(s) != 2:
        raise auth_access_token_no_valid_exception

    return s[0], s[1]
