from logging import getLogger
from traceback import format_exc

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

# from starlette_csrf import CSRFMiddleware

from traveling_sso.shared.schemas.exceptions import SsoException, SsoErrorCode
from .config import settings
from .database.deps import db_init_root_user
from .shared.schemas.protocol.error import SsoErrorsSchema, SsoErrorSchema
from .transport.rest import app_router


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

# if settings.CSRF_SECRET:
#     app.add_middleware(
#         CSRFMiddleware,
#         secret=settings.CSRF_SECRET
#     )


@app.exception_handler(SsoException)
async def sso_exception_handler(request: Request, exc: SsoException):
    logger.info(msg=exc)
    if settings.DEBUG:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=exc.error_code,
                    http_status_code=exc.http_status_code,
                    message=exc.message,
                    traceback=format_exc()
                )
            ]
        )
    else:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=exc.error_code
                )
            ]
        )

    return JSONResponse(
        status_code=exc.http_status_code if settings.DEBUG else status.HTTP_400_BAD_REQUEST,
        content=schema.model_dump()
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(exc, exc_info=exc)
    if settings.DEBUG:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=SsoErrorCode.GENERIC_ERROR,
                    http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error.",
                    traceback=format_exc()
                )
            ]
        )
    else:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=SsoErrorCode.GENERIC_ERROR
                )
            ]
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR if settings.DEBUG else status.HTTP_400_BAD_REQUEST,
        content=schema.model_dump()
    )


@app.on_event("startup")
async def startup():
    if settings.INIT_ROOT_ADMIN_USER:
        await db_init_root_user()
