from .error import SsoErrorCode, SsoException
from .templates import (
    client_not_found_exception,
    user_not_found_exception,
    user_role_not_found_exception,
    user_not_specified_exception,
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception
)

__all__ = (
    client_not_found_exception,
    user_not_found_exception,
    user_role_not_found_exception,
    user_not_specified_exception,
    passport_rf_not_specified_exception,
    foreign_passport_rf_not_specified_exception
)
