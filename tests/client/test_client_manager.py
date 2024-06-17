from typing import List

import allure
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.common.security import generate_token
from uuid_extensions import uuid7
from datetime import datetime, timedelta

from traveling_sso.database.models import Client, User
from traveling_sso.database.utils import utcnow


@allure.title("Get Client By ID")
@allure.feature("Client Management")
@allure.description("This test verifies the functionality of retrieving a client by ID from database.")
async def test_get_client_by_client_id(session: AsyncSession, client: Client):
    from traveling_sso.managers.client import get_client_by_client_id

    client_by_id = await get_client_by_client_id(
        session=session,
        client_id=client.client_id
    )
    assert client_by_id.client_id == client.client_id


@allure.title("Get Clients For User")
@allure.feature("Client Management")
@allure.description("This test verifies the functionality of getting a list of clients for a specific user.")
async def test_get_clients_for_user(session: AsyncSession, client: Client):
    from traveling_sso.managers.client import get_clients_for_user
    clients_for_user = await get_clients_for_user(session=session, user_id=client.user_id)

    assert isinstance(clients_for_user, List)
    assert len(clients_for_user) > 0
    assert not hasattr(clients_for_user[0], 'client_private_secret')
    assert clients_for_user[0].id == client.id
    assert clients_for_user[0].client_id == client.client_id
    assert clients_for_user[0].created_at == client.created_at
    assert clients_for_user[0].updated_at == client.updated_at
    assert clients_for_user[0].client_id_issued_at == client.client_id_issued_at
    assert clients_for_user[0].client_secret_expires_at == client.client_secret_expires_at
    assert clients_for_user[0].user.username == client.user.username
    assert clients_for_user[0].user.email == client.user.email


@allure.title("Create Client For User")
@allure.feature("Client Management")
@allure.description("This test verifies the functionality of creating a client for a specific user.")
async def test_create_client(session: AsyncSession, user: User):
    from traveling_sso.managers.client import create_client

    client_schema = await create_client(session=session, user=user)

    assert client_schema is not None
    assert str(client_schema.user.id) == str(user.id)
    assert client_schema.client_id is not None
    assert client_schema.client_public_secret is not None
    assert client_schema.client_id_issued_at is not None
    assert client_schema.client_secret_expires_at is not None


async def test_create_or_update_client(session: AsyncSession, user: User):
    from traveling_sso.managers.client import create_or_update_client
    from traveling_sso.managers.client import generate_pair_secrets_keys
    from traveling_sso.config import settings

    keys = generate_pair_secrets_keys()

    client_id_new = generate_token(48)
    client_private_secret_new = keys[1]
    client_id_issued_at_new = int(utcnow().timestamp())
    client_secret_expires_at_new = int((utcnow() + timedelta(days=settings.CLIENT_SECRET_EXPIRES_DAYS_IN)).timestamp())

    client_schema = await create_or_update_client(
        session=session,
        client_id=client_id_new,
        client_private_secret=client_private_secret_new,
        client_id_issued_at=client_id_issued_at_new,
        client_secret_expires_at=client_secret_expires_at_new,
        user=user
        )

    assert client_schema is not None
    assert client_schema.client_id == client_id_new
    assert client_schema.client_id_issued_at == client_id_issued_at_new
    assert client_schema.client_secret_expires_at == client_secret_expires_at_new
    assert str(client_schema.user.id) == str(user.id)


async def test_create_or_update_client_update(session: AsyncSession, user: User, client: Client):
    from traveling_sso.managers.client import create_or_update_client
    from traveling_sso.managers.client import generate_pair_secrets_keys
    from traveling_sso.config import settings

    keys = generate_pair_secrets_keys()

    client_id_new = generate_token(48)
    client_private_secret_new = keys[1]
    client_id_issued_at_new = int(utcnow().timestamp())
    client_secret_expires_at_new = int((utcnow() + timedelta(days=settings.CLIENT_SECRET_EXPIRES_DAYS_IN)).timestamp())

    client_schema = await create_or_update_client(
        session=session,
        client_id=client_id_new,
        client_private_secret=client_private_secret_new,
        client_id_issued_at=client_id_issued_at_new,
        client_secret_expires_at=client_secret_expires_at_new,
        user=user,
        id=client.id
        )

    assert client_schema is not None
    assert client_schema.id == client.id
    assert client_schema.client_id_issued_at == client.client_id_issued_at
    assert client_schema.client_secret_expires_at == client.client_secret_expires_at
    assert str(client_schema.user.id) == str(user.id)


async def test_generate_pair_secrets_keys():
    from traveling_sso.managers.client import generate_pair_secrets_keys

    keys = generate_pair_secrets_keys()

    assert keys is not None
    assert isinstance(keys, tuple)
    assert all(isinstance(i, str) for i in keys)