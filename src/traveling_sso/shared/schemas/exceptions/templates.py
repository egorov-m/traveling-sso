from starlette import status

from .error import SsoErrorCode, SsoException


client_not_found_exception = SsoException(
    message="Client not found exception.",
    error_code=SsoErrorCode.CLIENT_NOT_FOUND,
    http_status_code=status.HTTP_404_NOT_FOUND
)


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

user_not_specified_exception = SsoException(
    message="User not specified.",
    error_code=SsoErrorCode.USER_NOT_SPECIFIED,
    http_status_code=status.HTTP_400_BAD_REQUEST
)

user_conflict_exception = SsoException(
    message="User conflict.",
    error_code=SsoErrorCode.USER_NOT_SPECIFIED,
    http_status_code=status.HTTP_409_CONFLICT
)

passport_rf_not_specified_exception = SsoException(
    message="Passport RF not specified.",
    error_code=SsoErrorCode.DOCUMENT_PASSPORT_RF_NOT_SPECIFIED,
    http_status_code=status.HTTP_400_BAD_REQUEST
)

foreign_passport_rf_not_specified_exception = SsoException(
    message="Foreign passport RF not specified.",
    error_code=SsoErrorCode.DOCUMENT_FOREIGN_PASSPORT_RF_NOT_SPECIFIED,
    http_status_code=status.HTTP_400_BAD_REQUEST
)
