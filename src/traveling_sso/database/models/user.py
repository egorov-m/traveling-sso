from hashlib import sha512

from sqlalchemy import Column, Uuid, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from traveling_sso.shared.schemas.protocol import UserSchema
from .. import Base, TimeStampMixin
from ...config import settings


class User(Base, TimeStampMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(255), nullable=True, unique=True, index=True)

    role = Column(String(255), nullable=False)

    password_hash = Column(String(255), nullable=False)

    passport_rf_id = Column(ForeignKey("passport_rf.id", onupdate="SET NULL"), nullable=True)
    passport_rf = relationship("PassportRf", foreign_keys=[passport_rf_id])

    foreign_passport_rf_id = Column(ForeignKey("foreign_passport_rf.id", onupdate="SET NULL"), nullable=True)
    foreign_passport_rf = relationship("ForeignPassportRf", foreign_keys=[foreign_passport_rf_id])

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            email=self.email,
            username=self.username,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __init__(
            self,
            *,
            email: str,
            role: str,
            password: str,
            id: str | None = None,
            username: str | None = None,
            passport_rf_id: str | None = None,
            foreign_passport_rf_id: str | None = None
    ):
        if id:
            self.id = str(id)
        self.email = str(email)
        self.role = str(role)
        self.password_hash = self._get_password_hash(password)
        if username:
            self.username = username
        if passport_rf_id:
            self.passport_rf_id = str(passport_rf_id)
        if foreign_passport_rf_id:
            self.foreign_passport_rf_id = str(foreign_passport_rf_id)

    def check_password(self, password: str) -> bool:
        return self.password_hash == self._get_password_hash(password)

    @classmethod
    def _get_password_hash(cls, password: str) -> str:
        return sha512(
            password.encode("utf-8") + settings.AUTH_PASSWORD_SALT.encode("utf-8")
        ).hexdigest()
