---
title: Why use a JWT authentication middleware?
createTime: 2025-06-15 17:42
tags:
  - FastAPI
---

Authentication is essential in modern web apps. Let’s walk through fba’s JWT auth middleware in `backend/middleware/jwt_auth_middleware.py`, a best practice suitable for enterprise projects.

## What problems does it solve?

If you build an API that requires login, you need to:

* Verify identity
* Protect sensitive endpoints
* Maintain user context across requests
* Handle auth failures gracefully
* ...

Traditional approaches repeat auth code per route or rely on decorators. Our middleware integrates once and applies globally.

## How to use

In fba, middleware is registered centrally:

```python
def register_middleware(app: FastAPI) -> None:
    # ...other middleware
    app.add_middleware(
        AuthenticationMiddleware,
        backend=JwtAuthMiddleware(),
        on_error=JwtAuthMiddleware.auth_exception_handler,
    )
```

Then access the current user via `request.user` in route handlers:

```python
@router.get("/profile")
async def get_profile(request: Request):
    # user info injected by middleware
    current_user = request.user
    return {"user": current_user}
```

No verbose dependency injection or repeated auth code—clean and simple.

## How it differs from the official approach

FastAPI recommends `OAuth2PasswordBearer` with DI for JWT auth:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

Compared to our middleware, fewer lines don’t tell the full story:

1. Global consistency: all requests go through the same auth flow
2. Unified error handling: consistent response format for auth failures
3. Cleaner routes: no explicit auth dependencies; better separation of concerns
4. Extensible: easier to add new auth methods or permission checks

## Why recommend a JWT middleware?

This middleware-based approach has notable advantages:

### Developer-friendly

New team members don’t need to learn the auth internals—`request.user` holds the current user. Lowers onboarding cost and reduces potential security mistakes.

### Unified error handling

One handler processes all auth errors, ensuring consistent API responses. Whether token expired or malformed, clients get uniform messages.

### Performance considerations

Middleware runs auth logic only when needed and skips whitelisted paths (login, health checks, ...). It also uses Redis and a Rust lib to cache/parse user info for minimal overhead.

## Notes

The middleware is flexible for extensions, but applies to every API request (except unauthenticated and whitelisted). Consider applicability and performance for any additions.
