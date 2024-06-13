from .error import SsoErrorCode, SsoException
from .templates import (
    client_not_found_exception,
    user_not_found_exception,
    user_role_not_found_exception,
    user_not_specified_exception,
    user_conflict_exception,
    passport_rf_already_exists_exception,
    foreign_passport_rf_already_exists_exception,
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception,
    auth_unauthorized_exception,
    auth_access_denied_exception,
    auth_access_token_no_valid_exception,
    auth_refresh_token_no_valid_exception,
    auth_refresh_token_not_found_exception,
    validate_document_type_data_exception
)

__all__ = (
    client_not_found_exception,
    user_not_found_exception,
    user_role_not_found_exception,
    user_not_specified_exception,
    user_conflict_exception,
    passport_rf_already_exists_exception,
    foreign_passport_rf_already_exists_exception,
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception,
    auth_unauthorized_exception,
    auth_access_denied_exception,
    auth_access_token_no_valid_exception,
    auth_refresh_token_no_valid_exception,
    auth_refresh_token_not_found_exception,
    validate_document_type_data_exception
)
