from typing import Optional

from pydantic import Field
from starlette import status
from starlette.responses import JSONResponse

from traveling_sso.config import settings
from traveling_sso.shared.schemas.base import SsoBaseModel
from traveling_sso.shared.schemas.exceptions import SsoErrorCode


class SsoErrorSchema(SsoBaseModel):
    error_code: SsoErrorCode = Field(
        ...,
        description="Error code specifiable in sso. It is supposed to be used on the client for error handling."
    )
    http_status_code: Optional[int] = Field(
        None,
        description="Http status code, don't process this field on the client. It is used only in debug."
    )
    message: Optional[str | list | dict] = Field(
        None,
        description="A message describing the error. Don't use on the client, only for debug."
    )
    traceback: Optional[str] = Field(
        None,
        description="Traceback. Do not use on client, only in debug."
    )


class SsoErrorsSchema(SsoBaseModel):
    errors: list[SsoErrorSchema] = []


def get_error_response(
        *,
        error_code: SsoErrorCode = SsoErrorCode.GENERIC_ERROR,
        http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Internal Server Error.",
        traceback: str = ""
):
    if settings.DEBUG:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=error_code,
                    http_status_code=http_status_code,
                    message=message,
                    traceback=traceback
                )
            ]
        )
    else:
        schema = SsoErrorsSchema(
            errors=[
                SsoErrorSchema(
                    error_code=error_code
                )
            ]
        )

    return JSONResponse(
        status_code=http_status_code if settings.DEBUG else status.HTTP_400_BAD_REQUEST,
        content=schema.model_dump(exclude_unset=True),
    )
