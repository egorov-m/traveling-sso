from pydantic import Secret
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.exceptions import (
    user_conflict_exception,
    user_not_specified_exception
)
from traveling_sso.shared.schemas.protocol import (
    InternalCreateUserResponseSchema,
    UserRoleType,
    TokenResponseSchema,
    TokenType
)
from . import create_or_update_user, get_client_by_client_id
from .token import create_token_session
from ..database.models import User


class CustomAuthManager:
    def __init__(
            self,
            *,
            session: AsyncSession,
            password: Secret,
            client_id: str | None = None,
            email: str | None = None,
            username: str | None = None,
    ):
        self.session = session
        self.password = password
        self.client_id = client_id
        self.email = email
        self.username = username

        assert email is None or username is None, "Only one user identifier can be specified."

    async def signup(self) -> TokenResponseSchema | None:
        assert self.email is not None and self.password is not None, \
            "To signup, you need to specify your email address and password."

        query = select(User).where(User.email == self.email)
        user = (await self.session.execute(query)).scalar()
        if user is not None:
            raise user_conflict_exception

        user = await create_or_update_user(
            session=self.session,
            user_data=InternalCreateUserResponseSchema(
                role=UserRoleType.user,
                email=self.email,
                password=self.password
            )
        )

        if self.client_id is not None:
            client = await get_client_by_client_id(
                session=self.session,
                client_id=self.client_id
            )
            return await create_token_session(
                session=self.session,
                user=user,
                client=client,
                token_type=str(TokenType.Bearer)
            )
        else:
            return None

    async def signin(self) -> TokenResponseSchema:
        assert self.client_id is not None, "Requires client id to signin a user."

        query = select(User).where(User.email == self.email)
        user = (await self.session.execute(query)).scalar()
        if user is None:
            raise user_not_specified_exception

        client = await get_client_by_client_id(
            session=self.session,
            client_id=self.client_id
        )
        return await create_token_session(
            session=self.session,
            user=user,
            client=client,
            token_type=str(TokenType.Bearer)
        )
