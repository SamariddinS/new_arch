---
title: JWT
---

We have written JWT authorization middleware that can automatically authorize on each request. It also uses Redis and Rust
libraries to cache and parse user information, minimizing performance impact.

## API Authentication

In the file `backend/common/security/jwt.py`, the following code is included:

```python
# JWT authorizes dependency injection
DependsJwtAuth = Depends(CustomHTTPBearer())
```

We implement fast JWT validation by adding this dependency to API functions. It helps us check whether the request header contains a Bearer Token. Usage reference:

```python{1}
@router.get('/hello', summary='Hello', dependencies=[DependsJwtAuth])
async def hello():
    ...
```

## Token

Built-in token authorization follows [rfc6750](https://datatracker.ietf.org/doc/html/rfc6750)

## Swagger Login

This is a quick authorization method for debugging purposes only. After service startup, enter the Swagger docs to quickly obtain a token via this debug API (no captcha required).

## Captcha Login

You can obtain a token this way. In most cases, this is more suitable for implementing login authorization with a frontend.

We use [fast_captcha](https://github.com/wu-clan/fast-captcha) to generate base64 captchas in fba, then return data via API. You can preview by converting to images using online base64-to-image tools or with a frontend project. Below is its workflow:

```sequence Captcha login logic
actor Client
Client ->> Router: GET<br/>/api/v1/auth/captcha
Router ->> Rate Limiter: Verify request frequency
Rate Limiter -->> Router: Allow
Router ->> fast_captcha: Generate random captcha
fast_captcha ->> Redis: Cache captcha
Client ->> Router: POST<br/>/api/v1/auth/login
Router ->> Rate Limiter: Verify request frequency
Rate Limiter -->> Router: Allow
Router ->> Username: Verify username exists in system
Username -->> Router: Pass
Router ->> Captcha: Verify captcha (cache and image content)
Captcha -->> Router: Pass
Router ->> Token: Generate Token
Token -->> Client: Success
```
