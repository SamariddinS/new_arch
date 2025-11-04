---
title: How to write custom middleware?
createTime: 2024-10-31 18:30
tags:
  - FastAPI
---

Before writing middleware, let’s understand what it is.

## What is middleware?

Middleware is a mechanism to process requests and responses, automatically applied to every request.

Flow: when a request arrives, middleware runs before the route handler, allowing custom logic. Before the response is returned, middleware can also inspect/modify the response.

Common pitfall: a plain helper function placed in the middleware folder is not middleware. Put utilities in appropriate modules; middleware must integrate with the framework’s middleware interface.

## How to implement

Three ways to write middleware:

### BaseHTTPMiddleware

This is the simpler approach.

```python
class AccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        print(f'time: {end_time - start_time}')
        return response
```

Subclass `BaseHTTPMiddleware` and override `dispatch()`. Code before `call_next(request)` runs pre-handler; code after runs pre-response. Return the response.

### Pure ASGI

This is more complex.

```python
class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)
```

It follows the [ASGI spec](https://www.starlette.io/middleware/#pure-asgi-middleware). Without systematic study, implementing correctly is hard.

### Decorator

Looks convenient and appears in the FastAPI docs, but isn’t used in fba.

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = timezone.now()
    response = await call_next(request)
    end_time = timezone.now()
    print(f'time: {end_time - start_time}')
    return response
```

## How to use

In fba, open `backend/core/registrar.py` and find `register_middleware()`, which registers middleware.

Middleware executes from top to bottom; ordering matters.

FastAPI’s decorator internally calls `add_middleware()`. We add classes via `app.add_middleware()` directly, matching fba’s style.
