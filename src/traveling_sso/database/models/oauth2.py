from time import time

from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2AuthorizationCodeMixin, OAuth2TokenMixin
from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from .. import Base, TimeStampMixin


class OAuth2Client(Base, TimeStampMixin, OAuth2ClientMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])


class OAuth2AuthorizationCode(Base, OAuth2AuthorizationCodeMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])


class OAuth2Token(Base, OAuth2TokenMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)

    user_id = Column(ForeignKey("user.id", onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time()
