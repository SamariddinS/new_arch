from collections.abc import Callable
from functools import lru_cache

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.common.i18n import i18n


@lru_cache
def get_current_language(request: Request) -> str | None:
    """
    cRetrieve the language preference for the current request

    :param request: FastAPI Request Object
    :return:
    """
    accept_language = request.headers.get('Accept-Language', '')
    if not accept_language:
        return None

    languages = [lang.split(';')[0] for lang in accept_language.split(',')]
    lang = languages[0].lower().strip()

    # Language Mapping
    lang_mapping = {
        'ru': 'ru-RU',
        'ru-ru': 'ru-RU',
        'russian': 'ru-RU',
        'en': 'en-US',
        'en-us': 'en-US',
    }

    return lang_mapping.get(lang, lang)


class I18nMiddleware(BaseHTTPMiddleware):
    """Internationalized Middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process requests and configure internationalization languages

        :param request: FastAPI Request Object
        :param call_next: Next middleware or route handler
        :return:
        """
        language = get_current_language(request)

        # Set International Language
        if language and i18n.current_language != language:
            i18n.current_language = language

        response = await call_next(request)

        return response
