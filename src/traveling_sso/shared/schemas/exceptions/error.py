from enum import IntEnum

from starlette import status


class SsoErrorCode(IntEnum):
    """
    Error codes of the SSO API.

    Ranges:
            0-999: general errors
        1000-1999: auth errors
        2000-2999: client errors
        3000-3999: user errors
        4000-4999: documents errors
    """

    # 0-999: general errors
    GENERIC_ERROR = 0
    BASE_NOT_FOUND = 1
    VALIDATION_ERROR = 2

    # 1000-1999: auth errors
    AUTH_UNAUTHORIZED = 1000
    AUTH_FORBIDDEN = 1001
    AUTH_ACCESS_TOKEN_NO_VALID = 1002
    AUTH_REFRESH_TOKEN_NO_VALID = 1003
    AUTH_SESSION_NOT_FOUND = 1004

    # 2000-2999: client errors
    CLIENT_NOT_FOUND = 2000

    # 3000-3999: user errors
    USER_NOT_FOUND = 3000
    USER_ROLE_NOT_FOUND = 3001
    USER_NOT_SPECIFIED = 3002

    # 4000-4999: documents errors
    DOCUMENT_PASSPORT_RF_NOT_FOUND = 4000
    DOCUMENT_PASSPORT_RF_NOT_SPECIFIED = 4001
    DOCUMENT_PASSPORT_RF_ALREADY_EXIST_USER = 4002
    DOCUMENT_FOREIGN_PASSPORT_RF_NOT_FOUND = 4003
    DOCUMENT_FOREIGN_PASSPORT_RF_NOT_SPECIFIED = 4004
    DOCUMENT_FOREIGN_PASSPORT_RF_ALREADY_EXIST_USER = 4005


class SsoException(Exception):
    """Base class for SSO exceptions."""

    message: str
    error_code: int
    http_status_code: int

    def __init__(
            self,
            message: str,
            error_code: SsoErrorCode,
            http_status_code: int = status.HTTP_400_BAD_REQUEST,
            *args):
        super().__init__(message, error_code, http_status_code, *args)
        self.message = message
        self.error_code = error_code
        self.http_status_code = http_status_code

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (f"{class_name}(message=\"{self.message}\", error_code={self.error_code}, "
                f"http_status_code={self.http_status_code})")
