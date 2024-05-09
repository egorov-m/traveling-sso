from fastapi import APIRouter, Depends
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from traveling_sso.database.deps import get_db
from traveling_sso.shared.schemas.protocol import ClientSchema, UserSchema
from traveling_sso.transport.rest.app_deps import AuthSsoUser

client_router = APIRouter()


@client_router.post(
    "/create",
    response_model=ClientSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create SSO Client",
    description="Create sso client to get client id and client secrets."
)
async def create_client(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...


@client_router.get(
    "/get/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK,
    summary="Get client by Client ID"
)
async def get_client_by_client_id(
        client_id: constr(min_length=48, max_length=48),
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    # an admin can get any client, a normal user can only get his own client
    ...


@client_router.get(
    "/me/all",
    response_model=list[ClientSchema],
    status_code=status.HTTP_200_OK,
    summary="Get all me clients"
)
async def get_all_clients_for_user(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...
