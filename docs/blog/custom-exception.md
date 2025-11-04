---
title: How to define custom exceptions
createTime: 2025-01-26 16:43
tags:
  - FastAPI
---

fba provides a global exception handler that intercepts all errors and returns a standardized response body.

## Exception handler

The handler maps errors to standard status codes.

There are two codes in play: the HTTP response status code, and a business code in the response body. The HTTP code follows standards (e.g., 403 no permission, 404 not found) and can drive frontend routing. The business code is application-defined.

HTTP status codes follow RFC definitions; invalid ones fall back to 400.

```python
def _get_exception_code(status_code: int) -> int:
    """
    Retrieve the response status code (available status codes are based on RFC definitions)

    `Python Standard Support for HTTP Status Codes <https://github.com/python/cpython/blob/6e3cc72afeaee2532b4327776501eb8234ac787b/Lib/http/__init__.py#L7>`__

    `IANA Status Code Registry <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`__

    :param status_code: HTTP Status Codes
    :return:
    """
    try:
        STATUS_PHRASES[status_code]
        return status_code
    except Exception:
        return StandardResponseCode.HTTP_400
```

The handler covers: FastAPI validation errors, Pydantic validation errors, Python assert errors, unknown (unhandled) errors, CORS errors, and custom errors. See source: backend/common/exception/exception_handler.py

## Background tasks

Before custom errors, note this base mixin used by custom exceptions:

```python
class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None, background: BackgroundTask | None = None):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background
```

It supports a `background` parameter. FastAPI builds on Starlette, so you can use Starlette background tasks or FastAPI’s helpers interchangeably.

Note: background tasks attach to the response and run only after it is sent. Tasks run sequentially; if one fails, subsequent tasks won’t run. Use this only for small, safe tasks.

## Custom exceptions

See `backend/common/exception/errors.py` for built-in custom exceptions. They share a similar structure, for example:

```python
class NotFoundError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)
```

Commonly used: `code` is the HTTP status code. `msg` and `data` appear in the response body. `background` attaches background tasks as above.

Define your own:

```python
class CustomError(BaseExceptionMixin):
    code = 400  # RFC-compliant HTTP status

    def __init__(self, *, msg: str = 'Custom', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)
```

## Usage

Raise anywhere in fba code: `raise errors.XxxError(msg='...')`. The global handler formats and returns the response automatically.
