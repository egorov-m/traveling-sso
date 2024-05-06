from uuid import uuid4

from authlib.jose import jwt, RSAKey
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import TokenResponseSchema
from ..config import settings
from ..database.models import Client, TokenSession, User
from ..database.utils import utcnow


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
    header = {
        "alg": "RS512",
        "typ": "JWT"
    }
    payload = {
        "sub": user_id,
        "iss": "traveling-sso",
        "aud": "traveling service",
        "exp": int(utcnow().timestamp()) + settings.ACCESS_TOKEN_EXPIRES_IN,
        "role": user_role,
        "client_id": client_id,
        "session_id": str(uuid4())
    }
    token = jwt.encode(header, payload, RSAKey.import_key(secret).get_private_key())

    return token.decode("utf-8")
