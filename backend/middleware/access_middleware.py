import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.context import ctx
from backend.common.log import log
from backend.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """Access Logging Middleware"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process requests and log accesses

        :param request: FastAPI Request Object
        :param call_next: Next middleware or route handler
        :return:
        """
        path = request.url.path if not request.url.query else request.url.path + '/' + request.url.query

        if request.method != 'OPTIONS':
            log.debug(f'--> Request Start [{path}]')

        perf_time = time.perf_counter()
        ctx.perf_time = perf_time

        start_time = timezone.now()
        ctx.start_time = start_time

        response = await call_next(request)

        return response
