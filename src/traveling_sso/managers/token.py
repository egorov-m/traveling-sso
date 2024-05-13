from uuid import uuid4, UUID

from authlib.jose import RSAKey, JWTClaims as _JWTClaims, JsonWebToken
from authlib.jose.errors import JoseError
from sqlalchemy import select, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from traveling_sso.shared.schemas.protocol import TokenResponseSchema, UserSchema, UserRoleType, TokenSessionSchema
from traveling_sso.shared.schemas.exceptions.templates import (
    auth_access_token_no_valid_exception,
    auth_refresh_token_not_found_exception, auth_refresh_token_no_valid_exception
)
from ..config import settings
from ..database.models import Client, TokenSession, User
from ..database.utils import utcnow

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
        "user_role": {"essential": True},
        "session_id": {"essential": True}
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
    def factory_claims(cls, user_id, client_id, user_role, session_id) -> "JWTClaims":
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
                "user_role": user_role,
                "session_id": str(session_id)
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
    current_token_count = await get_count_active_token_session_for_user(session=session, user_id=user.id)

    if current_token_count >= settings.ACTIVE_REFRESH_TOKEN_MAX_COUNT:
        await revoke_all_active_token_sessions_for_user(
            session=session,
            user_id=user.id
        )

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
        str(user.id), user.role, client.client_id, client.client_private_secret, str(token.id)
    ))


def _get_active_token_sessions_for_user_whereclause(user_id):
    current_time = int(utcnow().timestamp())
    return [
        TokenSession.user_id == str(user_id),
        or_(TokenSession.refresh_token_revoked_at > current_time, TokenSession.refresh_token_revoked_at.is_(None)),
        TokenSession.issued_at + TokenSession.expires_in > current_time
    ]


async def get_token_session_by_session_id(*, session: AsyncSession, session_id: str) -> TokenSession:
    current_time = int(utcnow().timestamp())
    query = select(TokenSession).where(
        and_(
            TokenSession.id == session_id,
            or_(TokenSession.refresh_token_revoked_at > current_time, TokenSession.refresh_token_revoked_at.is_(None)),
            TokenSession.issued_at + TokenSession.expires_in > current_time
        )
    )
    token = (await session.execute(query)).scalar()
    if token is None:
        raise auth_refresh_token_not_found_exception

    return token


async def get_token_session_by_refresh_token(*, session: AsyncSession, refresh_token: str) -> TokenSession:
    current_time = int(utcnow().timestamp())
    query = select(TokenSession).where(
        and_(
            TokenSession.refresh_token == refresh_token,
            or_(TokenSession.refresh_token_revoked_at > current_time, TokenSession.refresh_token_revoked_at.is_(None)),
            TokenSession.issued_at + TokenSession.expires_in > current_time
        )
    )
    token = (await session.execute(query)).scalar()

    if token is None:
        raise auth_refresh_token_no_valid_exception

    return token


async def update_refresh_token(*, session: AsyncSession, token: TokenSession, client: Client, user: User) -> TokenResponseSchema:
    token.refresh_token = str(uuid4())
    session.add(token)
    await session.flush()

    return token.to_response_schema(access_token=generate_access_token(
        str(token.user_id), user.role, token.client_id, client.client_private_secret, str(token.id)
    ))


async def get_count_active_token_session_for_user(*, session: AsyncSession, user_id) -> int:
    query = select(count(TokenSession.id)).where(
        and_(*_get_active_token_sessions_for_user_whereclause(user_id))
    )
    tokens_count = (await session.execute(query)).scalar()

    return tokens_count


async def revoke_all_active_token_sessions_for_user(*, session: AsyncSession, user_id):
    current_time = int(utcnow().timestamp())
    query = update(TokenSession).where(
        and_(*_get_active_token_sessions_for_user_whereclause(user_id))
    ).values(refresh_token_revoked_at=current_time)
    await session.execute(query)
    await session.flush()


async def get_token_sessions_by_user_id(
        *,
        session: AsyncSession,
        user_id,
        current_session_id=None,
        client_id=None
) -> TokenSessionSchema:
    whereclause = _get_active_token_sessions_for_user_whereclause(user_id)
    if client_id is not None:
        whereclause.append(
            TokenSession.client_id == str(client_id)
        )
    query = select(TokenSession).where(and_(*whereclause))
    tokens = (await session.execute(query)).scalars().all()

    return [token.to_token_session_schema(token.id == current_session_id) for token in tokens]


async def revoke_token_session(
        *,
        session: AsyncSession,
        user: UserSchema,
        session_id: str | UUID
) -> bool:
    session_id = str(session_id)
    token = await get_token_session_by_session_id(session=session, session_id=session_id)
    if str(user.id) != token.user_id and user.role != UserRoleType.admin:
        raise auth_refresh_token_not_found_exception
    token.refresh_token_revoked_at = int(utcnow().timestamp())
    session.add(token)
    await session.commit()

    return True


def generate_access_token(user_id, user_role, client_id, secret, session_id):
    claims = JWTClaims.factory_claims(user_id, client_id, user_role, session_id)
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
