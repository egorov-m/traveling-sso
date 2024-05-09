from re import split

from sqlalchemy import Column, DateTime, event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, sessionmaker

from ..config import settings
from .utils import utcnow


engine: AsyncEngine = create_async_engine(url=settings.get_db_url(),
                                          pool_pre_ping=True,
                                          pool_size=settings.DB_POOL_SIZE,
                                          max_overflow=settings.DB_MAX_OVERFLOW)

get_session: sessionmaker = sessionmaker(engine, class_=AsyncSession)


class TimeStampMixin:
    """Timestamping mixin"""

    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)
