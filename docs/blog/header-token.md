---
title: How to authorize with a custom header token?
createTime: 2025-03-09 18:00
tags:
  - FastAPI
---

The official FastAPI advanced security guide introduces OAuth2 scopes and HTTP Basic Auth. Both enable Swagger UI authorization and allow quick login-based authorization within the docs.

While these approaches support quick validation in the docs, they rely on form-based login, which isn’t ideal for us. In fba we use HTTPBearer. It’s less convenient but still supports auto-authorization in the docs: first call the login endpoint to get a token, then paste it.

## Why Bearer Token?

In practice, many systems don’t use bearer tokens; authorization methods vary widely. Why bearer token then? Because it’s a standard scheme. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#authentication_schemes

Common API tools like Postman and Apifox support the bearer scheme, making auto-authorization easy. Refer to their docs for details.

## Custom token via header

Back to the point: how to use a non-bearer approach by putting a custom header for authorization.

First, open `backend/common/security/jwt.py` and change `DependsJwtAuth = Depends(HTTPBearer())` to `APIKeyHeader(name='xxx')`, where `name` is your custom header key. Since we originally used bearer, also update `get_token()` in the same file:

```python
def get_token(request: Request) -> str:
    token = request.headers.get('xxx')  # name
    if not token:
        raise TokenError(msg='Invalid token')
    return token
```

Then adjust the JWT middleware:

```python
# Remove the following lines
scheme, token = get_authorization_scheme_param(token)
if scheme.lower() != 'bearer':
    return
```

That completes custom token authorization. For the docs, you still need to log in first to obtain a token and paste it.

With this approach, API tools won’t auto-fill the header; you must add the token manually. For convenience, the standard bearer scheme is still recommended.
