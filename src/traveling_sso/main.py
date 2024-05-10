from logging import getLogger
from traceback import format_exc
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException, RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request

# from starlette_csrf import CSRFMiddleware

from traveling_sso.shared.schemas.exceptions import SsoException, SsoErrorCode
from traveling_sso.config import settings
from traveling_sso.database.deps import db_init_root_user
from traveling_sso.shared.schemas.protocol.error import get_error_response
from traveling_sso.transport.rest import app_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    servers=settings.API_SERVERS
)

app.include_router(app_router, prefix=settings.API_V1_STR)

logger = getLogger(settings.LOGGER_NAME)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    update_request_header=True,
    generator=lambda: uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)


# if settings.CSRF_SECRET:
#     app.add_middleware(
#         CSRFMiddleware,
#         secret=settings.CSRF_SECRET
#     )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationException):
    logger.info(msg=exc)
    return get_error_response(
        error_code=SsoErrorCode.VALIDATION_ERROR,
        http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=jsonable_encoder(exc.errors()),
        traceback=format_exc()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.info(msg=exc)
    return get_error_response(
        error_code=SsoErrorCode.GENERIC_ERROR,
        http_status_code=exc.status_code,
        message=exc.detail,
        traceback=format_exc()
    )


@app.exception_handler(SsoException)
async def sso_exception_handler(request: Request, exc: SsoException):
    logger.info(msg=exc)
    return get_error_response(
        error_code=exc.error_code,
        http_status_code=exc.http_status_code,
        message=exc.message,
        traceback=format_exc()
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(exc, exc_info=exc)
    return get_error_response(
        traceback=format_exc()
    )


@app.on_event("startup")
async def startup():
    if settings.INIT_ROOT_ADMIN_USER:
        await db_init_root_user()
