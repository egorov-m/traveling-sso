from datetime import timedelta

from authlib.jose import RSAKey
from authlib.common.security import generate_token
from cryptography.hazmat.primitives import serialization
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.protocol import ClientSchema
from traveling_sso.shared.schemas.exceptions import client_not_found_exception
from ..database.models import Client, User
from ..database.utils import utcnow
from ..config import settings


async def get_client_by_client_id(*, session: AsyncSession, client_id) -> Client:
    query = select(Client).where(Client.client_id == str(client_id))
    client = (await session.execute(query)).scalar()
    if client is None:
        raise client_not_found_exception

    return client


async def _get_client_by_uuid_id(session: AsyncSession, uuid_id: str):
    query = select(Client).where(Client.id == uuid_id)
    client = (await session.execute(query)).scalar()

    return client


async def get_clients_for_user(*, session: AsyncSession, user_id) -> list[ClientSchema]:
    query = select(Client).where(Client.user_id == str(user_id))
    clients = (await session.execute(query)).all()

    return [client.to_schema() for client in clients]


async def create_client(*, session: AsyncSession, user: User) -> ClientSchema:
    keys = _generate_pair_keys()

    client = Client(
        client_id=generate_token(48),
        client_public_secret=keys[0],
        client_private_secret=keys[1],
        client_id_issued_at=int(utcnow().timestamp()),
        client_secret_expires_at=int(
            (utcnow() + timedelta(days=settings.CLIENT_SECRET_EXPIRES_DAYS_IN)).timestamp()
        ),
        user=user
    )
    session.add(client)
    await session.flush()
    return client.to_schema()


async def create_or_update_client(
        *,
        session: AsyncSession,
        client_id: str,
        client_private_secret: str,
        client_id_issued_at: int,
        client_secret_expires_at: int,
        user: User,
        id: str | None = None
) -> ClientSchema:
    client = None
    if id is not None:
        client = await _get_client_by_uuid_id(session, id)
        if client is not None:
            _update_client_fields(client, {
                "client_id": client_id,
                "client_private_secret": client_private_secret,
                "client_id_issued_at": client_id_issued_at,
                "client_secret_expires_at": client_secret_expires_at,
                "user": user
            })
    if client is None:
        keys = _generate_pair_keys()
        client = Client(
            client_id=client_id or generate_token(48),
            client_private_secret=client_private_secret or keys[1],
            client_id_issued_at=client_id_issued_at or int(utcnow().timestamp()),
            client_secret_expires_at=client_secret_expires_at or int(
                (utcnow() + timedelta(days=settings.CLIENT_SECRET_EXPIRES_DAYS_IN)).timestamp()
            ),
            user=user,
            id=id
        )

    session.add(client)
    await session.flush()
    return client.to_schema()


def _generate_pair_keys() -> tuple[str, str]:
    rsa_key = (RSAKey.generate_key(settings.CLIENT_SECRET_KEY_SIZE, is_private=True))
    public_key = rsa_key.get_public_key()
    private_key = rsa_key.get_private_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_key_pem.decode("utf-8"), private_key_pem.decode("utf-8")


def _update_client_fields(client, fields: dict):
    for field, value in fields.items():
        if value is not None:
            setattr(client, field, value)
