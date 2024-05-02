from enum import IntEnum

from starlette import status


class SsoErrorCode(IntEnum):
    """
    Error codes of the SSO API.

    Ranges:
            0-999: general errors
        1000-1999: oauth errors
        2000-2999: client errors
        3000-3999: user errors
    """

    # 0-999: general errors
    GENERIC_ERROR = 0
    BASE_NOT_FOUND = 1

    # 1000-1999: oauth errors

    # 2000-2999: client errors

    # 3000-3999: user errors
    USER_NOT_FOUND = 2000
    USER_ROLE_NOT_FOUND = 2001
    USER_NOT_SPECIFIED = 2002


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
