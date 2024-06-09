from asyncio import get_event_loop_policy
from typing import AsyncGenerator

import allure
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .factories import UserFactory, ClientFactory, TokenSessionFactory
from traveling_sso.database.core import get_session
from traveling_sso.main import app


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


@pytest.fixture(scope="session")
@allure.title("Prepare SSO Service instance for tests.")
async def sso_service() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app) as sso_service:
        yield sso_service
