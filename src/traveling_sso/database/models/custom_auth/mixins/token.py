from time import time

from sqlalchemy import Column, String, BigInteger

from ....utils import utcnow


class _TokenMixin:
    def get_expires_in(self) -> int:
        """

        :return: int
        """
        raise NotImplementedError()

    def is_expired(self) -> bool:
        """

        :return: bool
        """
        raise NotImplementedError()

    def is_revoked(self) -> bool:
        """

        :return: bool
        """
        raise NotImplementedError()


class TokenMixin(_TokenMixin):
    """

    """

    client_id = Column(String(48), nullable=False)
    token_type = Column(String(40), nullable=False)
    refresh_token = Column(String(48), index=True, nullable=False)
    issued_at = Column(
        BigInteger, nullable=False, default=lambda: int(utcnow().timestamp())
    )
    refresh_token_revoked_at = Column(BigInteger, nullable=True)
    expires_in = Column(BigInteger, nullable=False)

    def get_expires_in(self) -> int:
        return self.expires_in

    def is_expired(self) -> bool:
        if not self.expires_in:
            return False

        expires_at = self.issued_at + self.expires_in
        return expires_at < time()

    def is_revoked(self) -> bool:
        return bool(self.refresh_token_revoked_at)
