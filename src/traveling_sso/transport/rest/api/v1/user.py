from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from traveling_sso.database.deps import get_db
from traveling_sso.shared.schemas.protocol import (
    UserSchema,
    PassportRfSchema,
    ForeignPassportRfSchema,
    CreatePassportRfResponseSchema,
    UpdatePassportRfResponseSchema,
    CreateForeignPassportRfResponseSchema,
    UpdateForeignPassportRfResponseSchema
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


@user_router.get(
    "/documents/passport_rf",
    response_model=PassportRfSchema,
    status_code=status.HTTP_200_OK,
    summary="Get Passport RF",
    description="Get passport data of the passport of the Russian Federation."
)
async def get_passport_rf(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...


@user_router.get(
    "/documents/foreign_passport_rf",
    response_model=ForeignPassportRfSchema,
    status_code=status.HTTP_200_OK,
    summary="Get Foreign Passport RF",
    description="Get passport data of the foreign passport of the Russian Federation."
)
async def get_foreign_passport_rf(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...


@user_router.get(
    "/documents/all",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get all documents",
    description="Get data of all added documents."
)
async def get_all_documents(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    """
    examples
    --------

    {
        "passport_rf": PassportRfSchema,
        "foreign_passport_rf": ForeignPassportRfSchema
    }

    {
        "passport_rf": PassportRfSchema,
        "foreign_passport_rf": None  # passport has not been added
    }
    """
    ...


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
    # TODO
    ...


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
        passport_rf: CreateForeignPassportRfResponseSchema = Body(
            ...,
            description="Foreign Passport data to be added."
        ),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...


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
    response_model=list,
    status_code=status.HTTP_200_OK,
    summary="Get user sessions"
)
async def get_sessions(
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    # TODO
    ...
