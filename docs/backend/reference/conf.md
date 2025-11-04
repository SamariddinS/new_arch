---
title: Configuration
---

The config file is `backend/core/conf.py`. All app and plugin settings in fba should live here.

## Environment

### `ENVIRONMENT` <Badge type="info" text="Literal['dev', 'prod']" /> <Badge type="warning" text="env" />

Environment mode. When `prod`, OpenAPI docs are disabled.

## FastAPI

### `FASTAPI_API_V1_PATH` <Badge type="info" text="str" />

API version prefix.

### `FASTAPI_TITLE` <Badge type="info" text="str" />

OpenAPI title.

### `FASTAPI_DESCRIPTION` <Badge type="info" text="str" />

OpenAPI description.

### `FASTAPI_DOCS_URL` <Badge type="info" text="str" />

Docs UI URL.

### `FASTAPI_REDOC_URL` <Badge type="info" text="str" />

ReDoc UI URL.

### `FASTAPI_OPENAPI_URL` <Badge type="info" text="str" />

OpenAPI JSON URL.

### `FASTAPI_STATIC_FILES` <Badge type="info" text="bool" />

Enable FastAPI static files service.

## Database

### `DATABASE_TYPE` <Badge type="info" text="Literal['postgresql', 'mysql']" /> <Badge type="warning" text="env" />

Database type: `postgresql` or `mysql`. Mind plugin compatibility.

### `DATABASE_HOST` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Database host.

### `DATABASE_PORT` <Badge type="info" text="int" /> <Badge type="warning" text="env" />

Database port.

### `DATABASE_USER` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Database username.

### `DATABASE_PASSWORD` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Database password.

### `DATABASE_ECHO` <Badge type="info" text="bool | Literal['debug']" />

Enable SQLAlchemy SQL logs.

### `DATABASE_POOL_ECHO` <Badge type="info" text="bool | Literal['debug']" />

Enable SQLAlchemy pool logs.

### `DATABASE_SCHEMA` <Badge type="info" text="str" />

Database/schema name.

### `DATABASE_CHARSET` <Badge type="info" text="str" />

Charset (MySQL only).

## Redis

### `REDIS_TIMEOUT` <Badge type="info" text="int" /> <Badge type="warning" text="env" />

Redis connection timeout.

### `REDIS_HOST` <Badge type="info" text="int" />

Redis host.

### `REDIS_PORT` <Badge type="info" text="str" />

Redis port.

### `REDIS_PASSWORD` <Badge type="info" text="int" />

Redis password.

### `REDIS_DATABASE` <Badge type="info" text="str" />

Default Redis logical database (0–15).

## Token

### `TOKEN_SECRET_KEY` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Secret key for token signing/parsing. Generate via `secrets.token_urlsafe(32)`.

::: danger
Keep this value safe to prevent attacks.
:::

### `TOKEN_ALGORITHM` <Badge type="info" text="str" />

Token algorithm.

### `TOKEN_EXPIRE_SECONDS` <Badge type="info" text="int" />

Token expiration in seconds.

### `TOKEN_REFRESH_EXPIRE_SECONDS` <Badge type="info" text="int" />

Refresh token expiration duration

### `TOKEN_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix for storing tokens in Redis

### `TOKEN_EXTRA_INFO_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix for storing token extension information in Redis

### `TOKEN_ONLINE_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix for storing token online status in Redis

### `TOKEN_REFRESH_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix for refreshing tokens stored in Redis

### `TOKEN_REQUEST_PATH_EXCLUDE` <Badge type="info" text="list[str]" />

JWT/RBAC Route Whitelist: Requests originating from addresses within this configuration will bypass token authenticity verification.

::: warning
Within FBA, parse the token using JWT middleware to retrieve user information and assign it to the FastAPI request object. If the route is included in this configuration,
`request.user` will be unavailable.
:::

### `TOKEN_REQUEST_PATH_EXCLUDE_PATTERN` <Badge type="info" text="list[Pattern[str]]" />

JWT/RBAC routing whitelist regular expression patterns match starting from the routing header. Requests matching these patterns will bypass token authenticity verification. Note: Same considerations apply as above.

## JWT Configuration

### `JWT_USER_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix for storing user information in Redis when JWT middleware stores it

## RBAC Configuration

[More details](./RBAC.md){.read-more}

### `RBAC_ROLE_MENU_MODE` <Badge type="info" text="bool" />

Whether to enable RBAC role menu mode

### `RBAC_ROLE_MENU_EXCLUDE` <Badge type="info" text="list[str]" />

When RBAC role menu mode is enabled, identifiers to skip RBAC authorization (when API permission identifiers match user menu permission identifiers)

## Cookie Configuration

### `COOKIE_REFRESH_TOKEN_KEY` <Badge type="info" text="str" />

Key name when storing refresh token in cookie

### `COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS` <Badge type="info" text="int" />

Expiration duration when storing refresh token in cookie

## Captcha Configuration

### `CAPTCHA_LOGIN_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when storing captcha in Redis during captcha login

### `CAPTCHA_LOGIN_EXPIRE_SECONDS` <Badge type="info" text="int" />

Captcha expiration duration during captcha login

## Data Permission Configuration

### `DATA_PERMISSION_MODELS` <Badge type="info" text="dict[str, str]" />

SQLA models allowed for data filtering. Model values must be defined as module strings

### `DATA_PERMISSION_COLUMN_EXCLUDE` <Badge type="info" text="list[str]" />

Exclude columns from SQLA models allowed for data filtering, e.g., id, password, etc.

## Socket.IO Configuration

### `WS_NO_AUTH_MARKER` <Badge type="info" text="str" />

Marker to skip user authentication when connecting to socket.io service. Should be defined directly as a token value for transmission

::: danger
Keep this value safe to prevent malicious attacks
:::

## CORS Configuration

### `CORS_ALLOWED_ORIGINS` <Badge type="info" text="list[str]" />

Allowed origins for cross-origin requests, without trailing `/`, e.g., `http://127.0.0.1:8000`

### `CORS_EXPOSE_HEADERS` <Badge type="info" text="list[str]" />

CORS exposed headers, allow adding this header to request headers

## Middleware Configuration

### `MIDDLEWARE_CORS` <Badge type="info" text="bool" />

Whether to enable CORS middleware

## Request Limiter Configuration

### `REQUEST_LIMITER_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when recording request frequency information in Redis

## Time Configuration

### `DATETIME_TIMEZONE` <Badge type="info" text="str" />

Global timezone

### `DATETIME_FORMAT` <Badge type="info" text="str" />

Format for converting time to time string

## File Upload Configuration

::: warning
Some configurations may be overridden by nginx
:::

### `UPLOAD_READ_SIZE` <Badge type="info" text="int" />

Buffer size for reading file content each time when uploading files

### `UPLOAD_IMAGE_EXT_INCLUDE` <Badge type="info" text="list[str]" />

Allowed image file types for upload

### `UPLOAD_IMAGE_SIZE_MAX` <Badge type="info" text="int" />

Maximum image file size allowed for upload

### `UPLOAD_VIDEO_EXT_INCLUDE` <Badge type="info" text="list[str]" />

Allowed video file types for upload

### `UPLOAD_VIDEO_SIZE_MAX` <Badge type="info" text="int" />

Maximum video file size allowed for upload

## Demo Mode Configuration

### `DEMO_MODE` <Badge type="info" text="bool" />

Whether to enable demo mode. When enabled, only `GET` and `OPTIONS` requests are allowed

### `DEMO_MODE_EXCLUDE` <Badge type="info" text="set[tuple[str, str]]" />

APIs excluded from request restrictions when demo mode is enabled

## IP Location Configuration

### `IP_LOCATION_PARSE` <Badge type="info" text="Literal['online', 'offline', 'false']" />

Mode for obtaining requester's location information

### `IP_LOCATION_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when storing location information in Redis

### `IP_LOCATION_EXPIRE_SECONDS` <Badge type="info" text="int" />

Location information cache duration

## Trace ID

### `TRACE_ID_REQUEST_HEADER_KEY` <Badge type="info" text="str" />

Trace ID request header key name

### `TRACE_ID_LOG_LENGTH` <Badge type="info" text="int" />

Trace ID log length, must be less than or equal to 32

### `TRACE_ID_LOG_DEFAULT_VALUE` <Badge type="info" text="str" />

Trace ID log default value

## Logging

### `LOG_FORMAT` <Badge type="info" text="str" />

Log content format (shared by console and file)

## Logging (Console)

### `LOG_STD_LEVEL` <Badge type="info" text="str" />

Log recording level

## Logging (File)

### `LOG_FILE_ACCESS_LEVEL` <Badge type="info" text="str" />

Access log recording level

### `LOG_FILE_ERROR_LEVEL` <Badge type="info" text="str" />

Error log recording level

### `LOG_ACCESS_FILENAME` <Badge type="info" text="str" />

Access log filename

### `LOG_ERROR_FILENAME` <Badge type="info" text="str" />

Error log filename

## Operation Log

### `OPERA_LOG_ENCRYPT_SECRET_KEY` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Operation log encryption key. Very important when using symmetric encryption algorithms to encrypt operation logs. Key generation:
`os.urandom(32).hex()`

::: danger
Keep this value safe to prevent malicious attacks
:::

### `OPERA_LOG_PATH_EXCLUDE` <Badge type="info" text="list[str]" />

Operation log path exclusions. Request addresses within this configuration will not record operation logs

### `OPERA_LOG_ENCRYPT_TYPE` <Badge type="info" text="int" />

Encryption type for API request parameters in operation logs

- 0: AES (performance overhead)
- 1: md5
- 2: ItsDangerous
- 3: No encryption
- others: Directly replace content with ******

### `OPERA_LOG_ENCRYPT_KEY_INCLUDE` <Badge type="info" text="list[str]" />

Encrypt API request parameters in operation logs

### `OPERA_LOG_QUEUE_BATCH_CONSUME_SIZE` <Badge type="info" text="int" />

Operation log queue batch consumption size. When limit is reached, operation logs will be batch written to database

### `OPERA_LOG_QUEUE_TIMEOUT` <Badge type="info" text="int" />

Operation log queue timeout duration. When limit is reached, operation logs will be batch written to database

## Plugin Configuration

### `PLUGIN_PIP_CHINA` <Badge type="info" text="bool" />

Whether to use domestic sources when downloading plugin dependencies via pip

### `PLUGIN_PIP_INDEX_URL` <Badge type="info" text="str" />

Index URL when downloading plugin dependencies via pip

### `PLUGIN_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when storing plugin information in Redis

## Application: Task

### `CELERY_BROKER_REDIS_DATABASE` <Badge type="info" text="int" /> <Badge type="warning" text="env" />

Redis logical database used by Celery broker

### `CELERY_RABBITMQ_HOST` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Host address for Celery to connect to RabbitMQ service

### `CELERY_RABBITMQ_PORT` <Badge type="info" text="int" /> <Badge type="warning" text="env" />

Host port number for Celery to connect to RabbitMQ service

### `CELERY_RABBITMQ_USERNAME` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Username for Celery to connect to RabbitMQ service

### `CELERY_RABBITMQ_PASSWORD` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Password for Celery to connect to RabbitMQ service

### `CELERY_BROKER` <Badge type="info" text="Literal['rabbitmq', 'redis']" />

Celery broker mode (dev mode defaults to Redis, prod mode forcibly switches to RabbitMQ)

### `CELERY_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when storing Celery data in Redis

### `CELERY_TASK_MAX_RETRIES` <Badge type="info" text="int" />

Maximum retry count when Celery task execution fails

## Plugin: Code Generator

#### `CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME` <Badge type="info" text="str" />

ZIP archive filename when downloading code

## Plugin: OAuth2

### `OAUTH2_GITHUB_CLIENT_ID` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

GitHub client ID

### `OAUTH2_GITHUB_CLIENT_SECRET` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

GitHub client secret

### `OAUTH2_GOOGLE_CLIENT_ID` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Google client ID

### `OAUTH2_GOOGLE_CLIENT_SECRET` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Google client secret

### `OAUTH2_LINUX_DO_CLIENT_ID` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Linux Do client ID

### `OAUTH2_LINUX_DO_CLIENT_SECRET` <Badge type="info" text="str" /> <Badge type="warning" text="env" />

Linux Do client secret

### `OAUTH2_GITHUB_REDIRECT_URI` <Badge type="info" text="str" />

GitHub redirect URI, must match GitHub OAuth Apps configuration

### `OAUTH2_GOOGLE_REDIRECT_URI` <Badge type="info" text="str" />

Google redirect URI, must match Google OAuth 2.0 client configuration

### `OAUTH2_LINUX_DO_REDIRECT_URI` <Badge type="info" text="str" />

Linux Do redirect URI, must match Linux Do Connect configuration

### `OAUTH2_FRONTEND_REDIRECT_URI` <Badge type="info" text="str" />

Frontend redirect URI after successful login

## Plugin: Email

### `EMAIL_USERNAME` <Badge type="info" text="str" />

Email sender user

### `EMAIL_PASSWORD` <Badge type="info" text="str" />

Email sender user password

### `EMAIL_HOST` <Badge type="info" text="str" />

Email service host address

### `EMAIL_PORT` <Badge type="info" text="int" />

Email service host port number

### `EMAIL_SSL` <Badge type="info" text="bool" />

Whether to enable SSL when sending emails

### `EMAIL_CAPTCHA_REDIS_PREFIX` <Badge type="info" text="str" />

Prefix when storing email verification code in Redis

### `EMAIL_CAPTCHA_EXPIRE_SECONDS` <Badge type="info" text="int" />

Email verification code cache duration
