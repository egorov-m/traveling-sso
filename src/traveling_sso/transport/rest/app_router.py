from fastapi import APIRouter
from starlette.responses import JSONResponse

from traveling_sso.transport.rest.api.v1 import custom_auth_router, user_router

app_router = APIRouter(
    default_response_class=JSONResponse
)

# app_router.include_router(client_router, prefix="/client", tags=["Client"])
app_router.include_router(custom_auth_router, prefix="/auth", tags=["Auth"])
app_router.include_router(user_router, prefix="/user/me", tags=["User (me)"])
