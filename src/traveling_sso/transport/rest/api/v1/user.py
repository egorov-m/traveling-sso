from typing import Literal

from fastapi import APIRouter, Depends, Body

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from traveling_sso.database.deps import get_db

from traveling_sso.managers.documents import create_passport_rf_new, create_foreign_passport_rf_new

from traveling_sso.managers import (
    get_passport_rf_by_user_id,
    get_foreign_passport_rf_by_user_id,
    get_token_sessions_by_user_id,
    get_all_documents_by_user_id,
    update_user
)

from traveling_sso.shared.schemas.protocol import (
    UserSchema,
    PassportRfSchema,
    ForeignPassportRfSchema,
    CreatePassportRfResponseSchema,
    UpdatePassportRfResponseSchema,
    CreateForeignPassportRfResponseSchema,
    UpdateForeignPassportRfResponseSchema,
    TokenSessionSchema,
    UserSessionSchema,
    UpdateUserInfoRequestSchema
)
from traveling_sso.transport.rest.app_deps import AuthSsoUser

user_router = APIRouter()


@user_router.get(
    "/info",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get Userinfo",
    description="Get base information about the user."
)
async def info(user: UserSchema = Depends(AuthSsoUser())):
    return user


@user_router.put(
    "/info",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Update Userinfo",
    description="Update base information about the user."
)
async def update_info(
        user_data: UpdateUserInfoRequestSchema,
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    user = await update_user(
        session=session,
        user_id=user.id,
        user_data=user_data
    )

    return user


@user_router.get(
    "/documents/passport_rf",
    response_model=PassportRfSchema | None,
    status_code=status.HTTP_200_OK,
    summary="Get Passport RF",
    description="Get passport data of the passport of the Russian Federation."
)
async def get_passport_rf(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    passport = await get_passport_rf_by_user_id(
            session=session,
            user_id=user.id
    )
    return passport


@user_router.get(
    "/documents/foreign_passport_rf",
    response_model=ForeignPassportRfSchema | None,
    status_code=status.HTTP_200_OK,
    summary="Get Foreign Passport RF",
    description="Get passport data of the foreign passport of the Russian Federation."
)
async def get_foreign_passport_rf(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    foreign_passport = await get_foreign_passport_rf_by_user_id(
        session=session,
        user_id=user.id
    )
    return foreign_passport


@user_router.get(
    "/documents/all",
    response_model=dict[Literal["passport_rf", "foreign_passport_rf"],
                        PassportRfSchema | ForeignPassportRfSchema | None] | None,
    status_code=status.HTTP_200_OK,
    summary="Get all documents",
    description="Get data of all added documents."
)
async def get_all_documents(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    documents = await get_all_documents_by_user_id(
        session=session,
        user_id=user.id
    )
    return documents


@user_router.post(
    "/documents/passport_rf",
    response_model=PassportRfSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Add Passport RF"
)
async def create_passport_rf(
        session: AsyncSession = Depends(get_db),
        passport_rf: CreatePassportRfResponseSchema = Body(..., description="Passport data to be added."),
        user: UserSchema = Depends(AuthSsoUser())
):
    user_id = str(user.id) if user else None
    new_passport_rf = await create_passport_rf_new(
        session=session,
        passport_data=passport_rf,
        user_id=user_id,
    )
    return new_passport_rf


@user_router.put(
    "/documents/passport_rf",
    response_model=PassportRfSchema,
    status_code=status.HTTP_200_OK,
    summary="Update Passport RF"
)
async def update_passport_rf(
        session: AsyncSession = Depends(get_db),
        passport_rf: UpdatePassportRfResponseSchema = Body(..., description="Passport data to be updated."),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    # update fields that are not None
    ...


@user_router.post(
    "/documents/foreign_passport_rf",
    response_model=ForeignPassportRfSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Add Foreign Passport RF"
)
async def create_foreign_passport_rf(
        session: AsyncSession = Depends(get_db),
        foreign_passport_rf: CreateForeignPassportRfResponseSchema = Body(
            ...,
            description="Foreign Passport data to be added."
        ),
        user: UserSchema = Depends(AuthSsoUser())
):
    user_id = str(user.id) if user else None
    new_foreign_passport_rf = await create_foreign_passport_rf_new(
        session=session,
        passport_data=foreign_passport_rf,
        user_id=user_id,
    )
    return new_foreign_passport_rf


@user_router.put(
    "/documents/foreign_passport_rf",
    response_model=ForeignPassportRfSchema,
    status_code=status.HTTP_200_OK,
    summary="Update Foreign Passport RF"
)
async def update_foreign_passport_rf(
        session: AsyncSession = Depends(get_db),
        passport_rf: UpdateForeignPassportRfResponseSchema = Body(
            ...,
            description="Foreign Passport data to be updated."
        ),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    # update fields that are not None
    ...


@user_router.get(
    "/sessions",
    response_model=list[TokenSessionSchema],
    status_code=status.HTTP_200_OK,
    summary="Get user sessions"
)
async def get_sessions(
        session: AsyncSession = Depends(get_db),
        user: UserSessionSchema = Depends(AuthSsoUser())
):
    return await get_token_sessions_by_user_id(
        session=session,
        user_id=user.id,
        current_session_id=user.session_id,
        client_id=user.client_id,
    )
