from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from traveling_sso.shared.schemas.exceptions.templates import auth_refresh_token_no_valid_exception
from traveling_sso.shared.schemas.exceptions import (
    user_conflict_exception,
    user_not_specified_exception,
    SsoException
)
from traveling_sso.shared.schemas.protocol import (
    InternalCreateUserRequestSchema,
    UserRoleType,
    TokenResponseSchema,
    TokenType
)
from . import (
    get_user_by_id,
    create_or_update_user,
    get_client_by_client_id,
    create_token_session,
    get_token_session_by_refresh_token,
    update_refresh_token
)
from ..database.models import User


class CustomAuthManager:
    def __init__(
            self,
            *,
            session: AsyncSession,
            password: str,
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

    @classmethod
    async def refresh(
            cls,
            *,
            session: AsyncSession,
            refresh_token: UUID | str
    ) -> TokenResponseSchema:
        token = await get_token_session_by_refresh_token(
            session=session,
            refresh_token=str(refresh_token)
        )
        try:
            client = await get_client_by_client_id(
                session=session,
                client_id=token.client_id
            )
            user = await get_user_by_id(
                session=session,
                user_id=token.user_id
            )
        except SsoException as error:
            raise auth_refresh_token_no_valid_exception from error

        return await update_refresh_token(
            session=session,
            token=token,
            client=client,
            user=user
        )

    async def signup(self) -> TokenResponseSchema | None:
        assert self.email is not None and self.password is not None, \
            "To signup, you need to specify your email address and password."

        query = select(User).where(User.email == self.email)
        user = (await self.session.execute(query)).scalar()
        if user is not None:
            raise user_conflict_exception

        user = await create_or_update_user(
            session=self.session,
            user_data=InternalCreateUserRequestSchema(
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
        user: User = (await self.session.execute(query)).scalar()
        if user is None or not user.check_password(self.password):
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
