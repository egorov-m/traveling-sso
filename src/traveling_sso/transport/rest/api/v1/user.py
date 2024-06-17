from functools import wraps

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from traveling_sso.database.deps import get_db
from traveling_sso.managers import (
    get_passport_rf_by_user_id,
    get_foreign_passport_rf_by_user_id,
    get_token_sessions_by_user_id,
    get_all_documents_by_user_id,
    update_user,
    create_passport_rf_new,
    create_foreign_passport_rf_new,
    update_passport_rf as _update_passport_rf,
    update_foreign_passport_rf as _update_foreign_passport_rf
)
from traveling_sso.shared.schemas.exceptions import validate_document_type_data_exception
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
    UpdateUserInfoRequestSchema,
    GetDocumentTypeSlug,
    DocumentType,
    DocumentTypeSlug
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


@user_router.patch(
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


def validate_document_type_data(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        document_type = kwargs.get("document_type")
        document_data = kwargs.get("document_data")

        if (
                document_type == DocumentTypeSlug.passport_rf and
                not isinstance(document_data, CreatePassportRfResponseSchema)
        ) or (
                document_type == DocumentTypeSlug.foreign_passport_rf and
                not isinstance(document_data, CreateForeignPassportRfResponseSchema)
        ):
            raise validate_document_type_data_exception

        return await func(*args, **kwargs)

    return wrapper


def _match_document_func(document_type, action_type):
    match document_type, action_type:
        case GetDocumentTypeSlug.passport_rf, "get":
            return get_passport_rf_by_user_id
        case GetDocumentTypeSlug.foreign_passport_rf, "get":
            return get_foreign_passport_rf_by_user_id
        case GetDocumentTypeSlug.all, "get":
            return get_all_documents_by_user_id
        case DocumentTypeSlug.passport_rf, "create":
            return create_passport_rf_new
        case DocumentTypeSlug.foreign_passport_rf, "create":
            return create_foreign_passport_rf_new
        case DocumentTypeSlug.passport_rf, "update":
            return _update_passport_rf
        case DocumentTypeSlug.foreign_passport_rf, "update":
            return _update_foreign_passport_rf
        case _, _:
            raise NotImplementedError("The document or action type isn't supported.")


@user_router.get(
    "/documents/{document_type}",
    response_model=(
            PassportRfSchema |
            ForeignPassportRfSchema |
            dict[
                DocumentType,
                PassportRfSchema |
                ForeignPassportRfSchema |
                None
            ] |
            None
    ),
    status_code=status.HTTP_200_OK,
    summary="Get Document",
    description="Get document data."
)
async def get_document(
        document_type: GetDocumentTypeSlug,
        session: AsyncSession = Depends(get_db),
        user: UserSchema = Depends(AuthSsoUser())
):
    get_document_func = _match_document_func(document_type, "get")
    result = await get_document_func(
        session=session,
        user_id=user.id
    )

    return result


@user_router.post(
    "/documents/{document_type}",
    response_model=PassportRfSchema | ForeignPassportRfSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Add document"
)
@validate_document_type_data
async def create_document(
        document_type: DocumentTypeSlug,
        session: AsyncSession = Depends(get_db),
        document_data: (
                CreatePassportRfResponseSchema |
                CreateForeignPassportRfResponseSchema
        ) = Body(..., description="Document data to be added."),
        user: UserSchema = Depends(AuthSsoUser())
):
    user_id = str(user.id)
    create_document_func = _match_document_func(document_type, "create")
    document = await create_document_func(
        session=session,
        passport_data=document_data,
        user_id=user_id
    )

    return document


@user_router.patch(
    f"/documents/{DocumentTypeSlug.passport_rf}",
    response_model=PassportRfSchema,
    status_code=status.HTTP_200_OK,
    summary="Update Passport RF"
)
async def update_passport_rf(
        session: AsyncSession = Depends(get_db),
        passport_rf: UpdatePassportRfResponseSchema = Body(..., description="Passport data to be updated."),
        user: UserSchema = Depends(AuthSsoUser())
):
    resp_schema = await _update_passport_rf(
        session=session,
        user_id=user.id,
        passport_data=passport_rf
    )

    return resp_schema


@user_router.patch(
    f"/documents/{DocumentTypeSlug.foreign_passport_rf}",
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
    resp_schema = await _update_foreign_passport_rf(
        session=session,
        user_id=user.id,
        passport_data=passport_rf
    )

    return resp_schema


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
