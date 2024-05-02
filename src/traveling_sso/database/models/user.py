from sqlalchemy import Column, Uuid, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from .. import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    """

    """

    id = Column(Uuid, default=uuid7, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(255), nullable=True, unique=True, index=True)

    role = Column(String(255), nullable=False)

    passport_rf_id = Column(ForeignKey("passport_rf.id", onupdate="SET NULL"), nullable=True)
    passport_rf = relationship("PassportRf", foreign_keys=[passport_rf_id])

    foreign_passport_rf_id = Column(ForeignKey("foreign_passport_rf.id", onupdate="SET NULL"), nullable=True)
    foreign_passport_rf = relationship("ForeignPassportRf", foreign_keys=[foreign_passport_rf_id])
