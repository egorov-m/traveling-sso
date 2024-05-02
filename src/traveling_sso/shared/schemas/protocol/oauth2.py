from enum import StrEnum

from pydantic import field_validator

from ..base import SsoBaseModel


class OAuth2ResponseType(StrEnum):
    code = "code"
    id_token = "id_token"


class OAuth2ScopeType(StrEnum):
    email = "email"
    profile = "profile"
    passport_rf = "passport_rf"
    foreign_passport_rf = "foreign_passport_rf"
