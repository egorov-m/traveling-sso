from traveling_sso.shared.schemas.base import SsoBaseModel


class AboutSchema(SsoBaseModel):
    name: str
    description: str
    version: str


class HealthSchema(SsoBaseModel):
    status: str
