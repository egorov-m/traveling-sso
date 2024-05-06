from typing import Annotated

from fastapi import APIRouter, Query, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from traveling_sso.database.deps import get_db
from traveling_sso.managers.custom_auth import CustomAuthManager
from traveling_sso.shared.schemas.protocol import TokenResponseSchema, SignInFormSchema
from traveling_sso.shared.schemas.protocol.custom_auth import SignUpFormSchema

custom_auth_router = APIRouter()


@custom_auth_router.post(
    "/signin",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="",
    description=""
)
async def signin(
       signin_form: SignInFormSchema,
        client_id: Annotated[str, Query(min_length=48, max_length=48, description="")],
        session: AsyncSession = Depends(get_db),
):
    kwargs = {
        "session": session,
        "password": signin_form.password.get_secret_value(),
        "client_id": client_id,
    }
    if signin_form.is_email():
        kwargs["email"] = signin_form.login
    else:
        kwargs["username"] = signin_form.login
    am = CustomAuthManager(**kwargs)

    return await am.signin()


@custom_auth_router.post(
    "/signup",
    response_model=TokenResponseSchema | None,
    status_code=status.HTTP_200_OK,
    summary="",
    description=""
)
async def signup(
        signup_form: SignUpFormSchema,
        client_id: Annotated[str | None, Query(
            ...,
            min_length=48,
            max_length=48,
            description="Transmit to get the tokens right away."
        )] = None,
        session: AsyncSession = Depends(get_db),
):
    am = CustomAuthManager(
        session=session,
        password=signup_form.password.get_secret_value(),
        client_id=client_id,
        email=signup_form.email
    )

    return await am.signup()
