from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Depends, Cookie, Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from traveling_sso.config import settings
from traveling_sso.database.deps import get_db
from traveling_sso.managers.custom_auth import CustomAuthManager
from traveling_sso.managers.token import revoke_token_session
from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception
from traveling_sso.shared.schemas.protocol import TokenResponseSchema, SignInFormSchema, UserSessionSchema
from traveling_sso.shared.schemas.protocol.custom_auth import SignUpFormSchema
from traveling_sso.transport.rest.app_deps import AuthSsoUser

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
        "password": signin_form.password,
        "client_id": client_id,
    }
    if signin_form.is_email():
        kwargs["email"] = signin_form.login
    else:
        kwargs["username"] = signin_form.login
    am = CustomAuthManager(**kwargs)

    res = await am.signin()
    if settings.IS_REFRESH_TOKEN_VIA_COOKIE:
        return res.to_response_with_cookie(
            cookie_name=settings.REFRESH_TOKEN_COOKIE_NAME,
            cookie_max_age=settings.REFRESH_TOKEN_EXPIRES_IN,
            cookie_path=settings.REFRESH_TOKEN_COOKIE_PATH,
        )
    else:
        return res


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
        password=signup_form.password,
        client_id=client_id,
        email=signup_form.email
    )

    res = await am.signup()
    if res is not None and settings.IS_REFRESH_TOKEN_VIA_COOKIE:
        return res.to_response_with_cookie(
            cookie_name=settings.REFRESH_TOKEN_COOKIE_NAME,
            cookie_max_age=settings.REFRESH_TOKEN_EXPIRES_IN,
            cookie_path=settings.REFRESH_TOKEN_COOKIE_PATH,
        )
    else:
        return res


@custom_auth_router.post(
    "/logout",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Logout session",
    description="A refresh token revoke will be performed, similar to `/session/revoke`."
)
async def logout(
        session: AsyncSession = Depends(get_db),
        user: UserSessionSchema = Depends(AuthSsoUser())
):
    return await revoke_token_session(
        session=session,
        user=user,
        session_id=user.session_id
    )


@custom_auth_router.post(
    "/session/revoke",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Revoke refresh token",
)
async def revoke_session(
        session_id: Annotated[UUID | None, Query(
            ...,
            description="Pass the session_id you want to revoke, otherwise the current token will be revoked.")
        ] = None,
        session: AsyncSession = Depends(get_db),
        user: UserSessionSchema = Depends(AuthSsoUser())
):
    if session_id is None:
        session_id = user.session_id

    return await revoke_token_session(
        session=session,
        user=user,
        session_id=session_id
    )


@custom_auth_router.post(
    "/session/refresh",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token"
)
async def refresh_session(
        refresh_token_header: str | None = Header(None, alias=settings.REFRESH_TOKEN_HEADER_NAME, description=""),
        refresh_token: str | None = Cookie(None, alias=settings.REFRESH_TOKEN_COOKIE_NAME, description=""),
        session: AsyncSession = Depends(get_db)
):
    if refresh_token is None:
        if refresh_token_header is not None:
            refresh_token = refresh_token_header
        else:
            raise auth_refresh_token_no_valid_exception

    res = await CustomAuthManager.refresh(
        session=session,
        refresh_token=refresh_token
    )
    if settings.IS_REFRESH_TOKEN_VIA_COOKIE:
        return res.to_response_with_cookie(
            cookie_name=settings.REFRESH_TOKEN_COOKIE_NAME,
            cookie_max_age=settings.REFRESH_TOKEN_EXPIRES_IN,
            cookie_path=settings.REFRESH_TOKEN_COOKIE_PATH,
        )
    else:
        return res
