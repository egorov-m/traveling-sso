from .client import client_router
from .custom_auth import custom_auth_router
from .user import user_router

__all__ = (
    client_router,
    custom_auth_router,
    user_router
)
