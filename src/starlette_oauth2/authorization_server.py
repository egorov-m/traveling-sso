from authlib.common.security import generate_token
from authlib.oauth2.rfc6750 import BearerTokenGenerator
from starlette.responses import JSONResponse
from authlib.oauth2 import (
    AuthorizationServer as _AuthorizationServer,
    OAuth2Request,
    JsonRequest
)

from .utils import import_string


class AuthorizationServer(_AuthorizationServer):
    """
        Starlette implementation of :class:`authlib.oauth2.rfc6749.AuthorizationServer`.
    """

    def __init__(self, app=None, query_client=None, save_token=None, scopes_supported=None):
        super().__init__(scopes_supported)
        self._query_client = query_client
        self._save_token = save_token
        self._error_uris = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, query_client=None, save_token=None):
        if query_client is not None:
            self._query_client = query_client
        if save_token is not None:
            self._save_token = save_token

        self.register_token_generator("default", self.create_bearer_token_generator(app.config))
        self.scopes_supported = app.config.get("OAUTH2_SCOPES_SUPPORTED")
        self._error_uris = app.config.get("OAUTH2_ERROR_URIS")

    def query_client(self, client_id):
        return self._query_client(client_id)

    def save_token(self, token, request):
        return self._save_token(token, request)

    def get_error_uri(self, request, error):
        if self._error_uris:
            uris = dict(self._error_uris)
            return uris.get(error.error)

    def create_oauth2_request(self, request):
        return OAuth2Request(
            request.method, str(request.url), request.body, request.headers
        )

    def create_json_request(self, request):
        return JsonRequest(
            request.method, str(request.url), request.body, request.headers
        )

    def handle_response(self, status_code, payload, headers):
        return JSONResponse(payload, status_code=status_code, headers=headers)

    def send_signal(self, name, *args, **kwargs):
        pass

    @classmethod
    def create_bearer_token_generator(cls, config: dict):
        """

        :param config:
        :return:
        """

        conf = config.get("OAUTH2_ACCESS_TOKEN_GENERATOR", True)
        access_token_generator = create_token_generator(conf, 42)

        conf = config.get("OAUTH2_REFRESH_TOKEN_GENERATOR", False)
        refresh_token_generator = create_token_generator(conf, 48)

        expires_conf = config.get("OAUTH2_TOKEN_EXPIRES_IN")
        expires_generator = create_token_expires_in_generator(expires_conf)
        return BearerTokenGenerator(
            access_token_generator,
            refresh_token_generator,
            expires_generator
        )


def create_token_expires_in_generator(expires_in_conf=None):
    if isinstance(expires_in_conf, str):
        return import_string(expires_in_conf)

    data = {}
    data.update(BearerTokenGenerator.GRANT_TYPES_EXPIRES_IN)
    if isinstance(expires_in_conf, dict):
        data.update(expires_in_conf)

    def expires_in(client, grant_type):
        return data.get(grant_type, BearerTokenGenerator.DEFAULT_EXPIRES_IN)

    return expires_in


def create_token_generator(token_generator_conf, length=42):
    """
        Create a token generator function.
    """
    if callable(token_generator_conf):
        return token_generator_conf

    if isinstance(token_generator_conf, str):
        return import_string(token_generator_conf)
    elif token_generator_conf is True:
        def token_generator(*args, **kwargs):
            return generate_token(length)
        return token_generator
