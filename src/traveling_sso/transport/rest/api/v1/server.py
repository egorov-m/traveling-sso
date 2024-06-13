from fastapi import APIRouter
from starlette import status

from traveling_sso.config import settings
from traveling_sso.shared.schemas.protocol import AboutSchema, HealthSchema


server_router = APIRouter()


@server_router.get(
    "/about",
    response_model=AboutSchema,
    status_code=status.HTTP_200_OK,
    summary="Get info about the server"
)
async def about():
    return AboutSchema(
        name=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION
    )


@server_router.get(
    "/health",
    response_model=HealthSchema,
    status_code=status.HTTP_200_OK,
    summary="Health Check"
)
def health():
    return HealthSchema(status="OK")
