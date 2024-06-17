import allure
from httpx import AsyncClient


BASE_PATH = "/api/v1/server"


@allure.title("Health check.")
@allure.feature("Server API")
async def test_health(sso_service: AsyncClient):
    resp = await sso_service.get(f"{BASE_PATH}/health")
    assert resp.status_code == 200


@allure.title("About.")
@allure.feature("Server API")
async def test_about(sso_service: AsyncClient):
    resp = await sso_service.get(f"{BASE_PATH}/about")
    assert resp.status_code == 200
