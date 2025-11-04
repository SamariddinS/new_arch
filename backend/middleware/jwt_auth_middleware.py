from typing import Any

from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.common.exception.errors import TokenError
from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse


class _AuthenticationError(AuthenticationError):
    """Rewrite Internal Authentication Error Class"""

    def __init__(
        self,
        *,
        code: int | None = None,
        msg: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialization authentication error

        :param code: Error code
        :param msg: Error message
        :param headers: Response headers
        :return:
        """
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT Authentication Middleware"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticationError) -> Response:
        """
        Cover internal authentication error handling

        :param conn: HTTP Connecting objects
        :param exc: Authentication Error Object
        :return:
        """
        return MsgSpecJSONResponse(content={'code': exc.code, 'msg': exc.msg, 'data': None}, status_code=exc.code)

    async def authenticate(self, request: Request) -> tuple[AuthCredentials, GetUserInfoWithRelationDetail] | None:
        """
        Certification Request

        :param request: FastAPI Request Object
        :return:
        """
        token = request.headers.get('Authorization')
        if not token:
            return None

        path = request.url.path
        if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return None
        for pattern in settings.TOKEN_REQUEST_PATH_EXCLUDE_PATTERN:
            if pattern.match(path):
                return None

        scheme, token = get_authorization_scheme_param(token)
        if scheme.lower() != 'bearer':
            return None

        try:
            user = await jwt_authentication(token)
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.exception(f'JWT Authorization Exception: {e}')
            raise _AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # Please note that this return uses a non-standard mode, so certain standard features will be lost upon successful authentication.
        # For standard return procedures, please refer to: https://www.starlette.io/authentication/
        return AuthCredentials(['authenticated']), user
