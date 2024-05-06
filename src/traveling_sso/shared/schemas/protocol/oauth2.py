from typing import Optional
from enum import StrEnum
from uuid import UUID

from pydantic import SecretStr, constr, Field

from ..base import SsoBaseModel


class OAuth2ResponseType(StrEnum):
    code = "code"
    id_token = "id_token"


class OAuth2ScopeType(StrEnum):
    email = "email"
    profile = "profile"
    passport_rf = "passport_rf"
    foreign_passport_rf = "foreign_passport_rf"


class OAuth2TokenType(StrEnum):
    Bearer = "Bearer"


class OAuth2AuthorizeResponseSchema(SsoBaseModel):
    code: Optional[constr(min_length=48, max_length=48)] = None
    id_token: Optional[SecretStr[str]] = None


class OAuth2TokenResponseSchema(SsoBaseModel):
    access_token: constr(min_length=48, max_length=48)
    token_type: OAuth2TokenType = OAuth2TokenType.Bearer
    expires_in: int
    # refresh_token: constr(min_length=48, max_length=48)


class OAuthIntrospectResponseSchema(SsoBaseModel):
    active: bool = False
    client_id: constr(min_length=48, max_length=48)
    sub: UUID = Field(..., description="User id.")
