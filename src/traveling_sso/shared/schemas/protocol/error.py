from typing import Optional

from pydantic import Field

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
    message: Optional[str] = Field(
        None,
        description="A message describing the error. Don't use on the client, only for debug."
    )
    traceback: Optional[str] = Field(
        None,
        description="Traceback. Do not use on client, only in debug."
    )


class SsoErrorsSchema(SsoBaseModel):
    errors: list[SsoErrorSchema] = []
