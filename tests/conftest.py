from asyncio import get_event_loop_policy
from typing import AsyncGenerator
from uuid import uuid4

import allure
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.main import app
from traveling_sso.config import settings
from traveling_sso.database.core import get_session

from factories import UserFactory, ClientFactory, TokenSessionFactory
from utils import validate_token_schema, validate_sessions_list


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
@allure.title("Prepare database session for the test.")
async def session():
    session: AsyncSession = get_session()
    async with session.begin() as transaction:
        yield session


@pytest.fixture()
@allure.title("Prepare user in database for the test.")
async def user(session):
    return await UserFactory(session)


@pytest.fixture()
@allure.title("Prepare sso client in database for the test.")
async def client(session):
    return await ClientFactory(session)


@pytest.fixture()
@allure.title("Prepare refresh token session in database for the test.")
async def token_session(session, client):
    return await TokenSessionFactory(session, client_id=client.client_id)


# Fixtures for api testing _____________________________________________________________________________________________

@pytest.fixture
@allure.title("Prepare SSO Service instance for tests.")
async def sso_service() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(
                app=app,
                client=(settings.SSO_HOST, settings.SSO_PORT)
            ),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
@allure.title("Prepare SSO service admin user session.")
async def sso_admin_token(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"/api/v1/auth/signin?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "login": settings.ROOT_ADMIN_USER["email"],
            "password": settings.ROOT_ADMIN_USER["password"]
        }
    )
    assert resp.status_code == 200
    token = validate_token_schema(resp)

    return token


@pytest.fixture
@allure.title("Prepare SSO service user session.")
async def sso_token(sso_service: AsyncClient):
    resp = await sso_service.post(
        f"/api/v1/auth/signup?client_id={settings.ROOT_ADMIN_USER_CLIENT['client_id']}",
        json={
            "email": f"{uuid4().hex}@example.com",
            "password": str(uuid4())
        }
    )
    assert resp.status_code == 200
    token = validate_token_schema(resp)

    return token


@pytest.fixture
@allure.title("Prepare SSO service admin user sessions list.")
async def sso_get_admin_sessions(sso_service: AsyncClient, sso_admin_token):
    resp = await sso_service.get(
        "/api/v1/user/me/sessions",
        headers={
            "Authorization": f"Bearer {sso_admin_token.access_token}"
        }
    )
    data = validate_sessions_list(resp)

    return data


@pytest.fixture
@allure.title("Prepare SSO service user sessions list.")
async def sso_get_sessions(sso_service: AsyncClient, sso_token):
    resp = await sso_service.get(
        "/api/v1/user/me/sessions",
        headers={
            "Authorization": f"Bearer {sso_token.access_token}"
        }
    )
    data = validate_sessions_list(resp)

    return data
