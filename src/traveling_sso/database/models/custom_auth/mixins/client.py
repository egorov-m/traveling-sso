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
    client_private_secret = Column(String, nullable=False)
    client_id_issued_at = Column(BigInteger, nullable=False)
    client_secret_expires_at = Column(BigInteger, nullable=False)
