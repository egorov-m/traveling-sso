from secrets import compare_digest

from sqlalchemy import Column, BigInteger, String


class _ClientMixin:
    """

    """

    def check_client_secret(self, client_secret) -> bool:
        """

        :param client_secret: A string of client secret
        :return: bool
        """
        raise NotImplementedError()


class ClientMixin(_ClientMixin):
    """

    """

    client_id = Column(String(48), index=True, unique=True, nullable=False)
    client_public_secret = Column(String, nullable=False)
    client_private_secret = Column(String, nullable=False)
    client_id_issued_at = Column(BigInteger, nullable=False)
    client_secret_expires_at = Column(BigInteger, nullable=False)

    @property
    def client_info(self) -> dict:
        """

        :return: dict
        """
        return dict(
            client_id=self.client_id,
            client_public_secret=self.client_public_secret,
            client_private_secret=self.client_private_secret,
            client_id_issued_at=self.client_id_issued_at,
            client_secret_expires_at=self.client_secret_expires_at
        )

    def check_client_secret(self, client_secret) -> bool:
        """

        :param client_secret: A string of client secret
        :return: bool
        """
        self.client_public_secret: str
        return compare_digest(self.client_public_secret, client_secret)
