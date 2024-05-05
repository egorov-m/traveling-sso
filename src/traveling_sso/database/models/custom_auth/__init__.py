from uuid import UUID

from sqlalchemy import (
    Column,
    Uuid,
    String,
    ForeignKey,
    insert,
    UniqueConstraint,
    and_
)
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from traveling_sso.shared.schemas.exceptions import user_not_found_exception
from traveling_sso.shared.schemas.protocol import ClientSchema
from ... import TimeStampMixin, Base
from .mixins import ClientMixin, TokenMixin


class Client(Base, TimeStampMixin, ClientMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    def to_schema(self) -> ClientSchema:
        return ClientSchema(
            id=self.id,
            client_id=self.client_id,
            client_public_secret=self.client_public_secret,
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
            client_public_secret: str,
            client_private_secret: str,
            client_id_issued_at: int,
            client_secret_expires_at: int,
            id: str | None = None,
            **kwargs
    ):
        self.client_id = client_id
        self.client_public_secret = client_public_secret
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


class TokenAgent(Base, TimeStampMixin):
    """

    """

    __table_args__ = (
        UniqueConstraint("token_session_id", "fingerprint", "user_agent", "ip_address"),
    )

    id = Column(Uuid, default=uuid7, primary_key=True)
    token_session_id = Column(ForeignKey("token_session.id", onupdate="CASCADE"), nullable=False)
    fingerprint = Column(String(40), nullable=True, default=None)
    user_agent = Column(String(255), nullable=True, default=None)
    ip_address = Column(String(80), nullable=False)

    @classmethod
    async def get_or_create(
            cls,
            token_session_id,
            ip_address,
            fingerprint=None,
            user_agent=None
    ) -> tuple["TokenAgent", bool]:
        is_new = False
        query = select(cls).where(
            and_(
                cls.token_session_id == token_session_id,
                cls.ip_address == ip_address,
                cls.fingerprint == fingerprint,
                cls.user_agent == user_agent
            )
        )
        agent = None  # await db.fetch_one(query)

        if agent is not None:
            is_new = True
            query = insert(cls).values({
                "token_session_id": token_session_id,
                "ip_address": ip_address,
                "fingerprint": fingerprint
            }).returning(cls)
            # agent = await db.execute(query)

        return agent, is_new
