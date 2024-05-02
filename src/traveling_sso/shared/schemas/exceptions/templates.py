from starlette import status

from .error import SsoErrorCode, SsoException


user_not_found_exception = SsoException(
    message="User not found.",
    error_code=SsoErrorCode.USER_NOT_FOUND,
    http_status_code=status.HTTP_404_NOT_FOUND
)

user_role_not_found_exception = SsoException(
    message="User role not found.",
    error_code=SsoErrorCode.USER_ROLE_NOT_FOUND,
    http_status_code=status.HTTP_404_NOT_FOUND
)
