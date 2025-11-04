---
title: CORS
---

When integrating frontend and backend locally or deploying to servers, you’ll often hit CORS issues. Edit `core/conf.py` and set `CORS_ALLOWED_ORIGINS` to resolve them.

## Local

```py
CORS_ALLOWED_ORIGINS: list[str] = [
        'http://localhost:5173',  # Frontend URL without trailing '/'
    ]
```

## Server

::: code-tabs
@tab <Icon name="arcticons:http-custom" />HTTP

```py
# [!code word:http]
CORS_ALLOWED_ORIGINS: list[str] = [
      'http://<server-ip>:<port>',  # Frontend URL without '/', omit port if 80
  ]
```

@tab <Icon name="ic:outline-https" /> HTTPS

```py
# [!code word:https]
CORS_ALLOWED_ORIGINS: list[str] = [
      'https://<domain>',  # Frontend URL without '/'
  ]
```

:::

## LAN

Depends on whether the frontend project serves on LAN.

```py
CORS_ALLOWED_ORIGINS: list[str] = ['*']
```
