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

passport_rf_already_exists_exception = SsoException(
    message="Passport RF already exists.",
    error_code=SsoErrorCode.DOCUMENT_PASSPORT_RF_NOT_SPECIFIED,
    http_status_code=status.HTTP_400_BAD_REQUEST
)

foreign_passport_rf_already_exists_exception = SsoException(
    message="Foreign passport RF already exists.",
    error_code=SsoErrorCode.DOCUMENT_PASSPORT_RF_NOT_SPECIFIED,
    http_status_code=status.HTTP_400_BAD_REQUEST
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

auth_unauthorized_exception = SsoException(
    message="Could not validate credentials.",
    error_code=SsoErrorCode.AUTH_UNAUTHORIZED,
    http_status_code=status.HTTP_401_UNAUTHORIZED
)

auth_access_denied_exception = SsoException(
    message="Access denied.",
    error_code=SsoErrorCode.AUTH_FORBIDDEN,
    http_status_code=status.HTTP_403_FORBIDDEN
)

auth_access_token_no_valid_exception = SsoException(
    message="Access token no valid.",
    error_code=SsoErrorCode.AUTH_ACCESS_TOKEN_NO_VALID,
    http_status_code=status.HTTP_403_FORBIDDEN
)

auth_refresh_token_no_valid_exception = SsoException(
    message="Refresh token no valid.",
    error_code=SsoErrorCode.AUTH_REFRESH_TOKEN_NO_VALID,
    http_status_code=status.HTTP_403_FORBIDDEN
)

auth_session_not_found_exception = SsoException(
    message="Refresh token not found.",
    error_code=SsoErrorCode.AUTH_SESSION_NOT_FOUND,
    http_status_code=status.HTTP_404_NOT_FOUND
)

validate_document_type_data_exception = SsoException(
    message="Document type and data don't match.",
    error_code=SsoErrorCode.VALIDATION_ERROR,
    http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
)
