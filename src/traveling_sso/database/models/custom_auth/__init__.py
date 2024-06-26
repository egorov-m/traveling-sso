from authlib.jose import RSAKey
from cryptography.hazmat.primitives import serialization
from sqlalchemy import (
    Column,
    Uuid,
    ForeignKey
)
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from traveling_sso.shared.schemas.protocol import ClientSchema, TokenResponseSchema
from traveling_sso.shared.schemas.protocol.custom_auth import TokenSessionSchema
from ... import TimeStampMixin, Base
from .mixins import ClientMixin, TokenMixin


class Client(Base, TimeStampMixin, ClientMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    def to_schema(self) -> ClientSchema:
        rsa_public_key = RSAKey.import_key(self.client_private_secret).get_public_key()
        client_public_secret = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

        return ClientSchema(
            id=self.id,
            client_id=self.client_id,
            client_public_secret=client_public_secret,
            client_id_issued_at=self.client_id_issued_at,
            client_secret_expires_at=self.client_secret_expires_at,
            user=self.user.to_schema(),
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __init__(
            self,
            *,
            client_id: str,
            client_private_secret: str,
            client_id_issued_at: int,
            client_secret_expires_at: int,
            id: str | None = None,
            **kwargs
    ):
        self.client_id = client_id
        self.client_private_secret = client_private_secret
        self.client_id_issued_at = client_id_issued_at
        self.client_secret_expires_at = client_secret_expires_at
        if id:
            self.id = id
        super().__init__(**kwargs)


class TokenSession(Base, TimeStampMixin, TokenMixin):
    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    def is_refresh_token_active(self) -> bool:
        return not (self.is_revoked() or self.is_expired())

    def to_response_schema(self, access_token) -> TokenResponseSchema:
        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=self.refresh_token,
            token_type=self.token_type,
            expires=self.issued_at + self.expires_in
        )

    def to_token_session_schema(self, is_current: bool = False) -> TokenSessionSchema:
        return TokenSessionSchema(
            session_id=self.id,
            issued_at=self.issued_at,
            expires_at=self.issued_at + self.expires_in,
            is_current=is_current
        )
