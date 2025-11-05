# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI Best Architecture (FBA) is an enterprise-level backend architecture solution implementing a 3-tier architecture pattern with RBAC (Role-Based Access Control) permission control system.

**Architecture Pattern (Java → FBA mapping):**
- View (controller) → api
- Data transmit (dto) → schema
- Business logic (service + impl) → service
- Data access (dao/mapper) → crud
- Model (model/entity) → model

## Development Commands

### Initial Setup

1. **Install dependencies** (requires `uv` package manager):
   ```bash
   uv sync
   # or
   uv pip install -r requirements.txt
   ```

2. **Environment configuration**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and backend/core/conf.py as needed
   ```

3. **Database setup**:
   - Create database named `fba` (utf8mb4 charset for MySQL)
   - Tables are auto-created on first run, or use Alembic:
     ```bash
     cd backend
     alembic revision --autogenerate
     alembic upgrade head
     ```

4. **Seed test data**:
   - Run SQL scripts from `backend/sql/` for your PK mode
   - For plugins: run scripts from `backend/plugin/*/sql/`
   - Use CLI to execute SQL scripts:
     ```bash
     # Main test data
     fba --sql backend/sql/init_test_data.sql

     # Config plugin
     fba --sql backend/plugin/config/sql/postgresql/init.sql

     # Dict plugin
     fba --sql backend/plugin/dict/sql/postgresql/init.sql
     ```

### Running the Application

```bash
# Run API server from repo root
fba run

# With custom host/port
fba run 0.0.0.0 9000

# Disable auto-reload (for production)
fba run --no-reload

# Multiple workers (requires --no-reload)
fba run --no-reload --workers 4
```

### Celery Task Services (Optional)

```bash
# Start worker
fba celery worker

# Start beat scheduler
fba celery beat

# Start flower monitoring
fba celery flower
```

**Important:** Task result tables won't exist until worker/beat run at least once. APIs touching task results will error until then.

### Testing

```bash
# Create test database: fba_test (utf8mb4 for MySQL)
# Populate with test data from backend/sql/
pytest -vs --disable-warnings
```

### Plugin Management

```bash
# Install from local ZIP
fba add /path/to/plugin.zip

# Install from Git repository
fba add <git_repo_url>

# Skip SQL script auto-execution
fba add /path/to/plugin.zip --no-sql
```

### Code Generation

```bash
# Import database table for code generation
fba codegen import <app_name> --tn <table_name>

# Generate code from imported tables
fba codegen
```

## Architecture & Code Organization

### Application Structure

```
backend/
├── app/                    # Applications (e.g., admin, task)
│   ├── admin/
│   │   ├── api/           # API routes (view layer)
│   │   │   ├── v1/        # Version 1 endpoints
│   │   │   │   ├── auth/  # Auth routes
│   │   │   │   ├── sys/   # System routes
│   │   │   │   └── log/   # Logging routes
│   │   │   └── router.py  # Main router registration
│   │   ├── crud/          # Database operations (data access layer)
│   │   ├── model/         # SQLAlchemy models
│   │   ├── schema/        # Pydantic schemas (data transfer layer)
│   │   └── service/       # Business logic layer
│   └── router.py          # App-level router registration
├── common/                # Shared utilities
│   ├── exception/         # Error handling
│   ├── response/          # Response models
│   ├── security/          # JWT, RBAC, permissions
│   ├── i18n.py           # Internationalization
│   ├── log.py            # Logging configuration
│   ├── model.py          # Base models & mixins
│   └── pagination.py     # Pagination utilities
├── core/                  # Core configuration
│   ├── conf.py           # Global settings (Pydantic Settings)
│   └── registrar.py      # App registration
├── database/              # Database connections
│   ├── db.py             # SQLAlchemy async engine/session
│   └── redis.py          # Redis configuration
├── middleware/            # Request/response middleware
│   ├── jwt_auth_middleware.py    # JWT authentication
│   ├── i18n_middleware.py        # Language detection
│   ├── access_middleware.py      # Access control
│   ├── opera_log_middleware.py   # Operation logging
│   └── state_middleware.py       # Request state
├── locale/               # i18n language files (JSON/YAML)
├── sql/                  # Database initialization scripts
├── cli.py               # CLI commands (fba command)
└── main.py              # FastAPI application entry
```

### Router Structure & Registration

- API routers are in `app/*/api/v1/` directories
- All router parameters are named `router` - use import aliases to avoid conflicts:
  ```python
  from backend.app.admin.api.v1.sys.user import router as user_router
  ```
- Router registration flows:
  - Individual route files → subpackage `__init__.py` → `router.py` (app level) → `backend/app/router.py` (global)

### Database Configuration

**Location:** `backend/core/conf.py` and `.env`

**Supported databases:**
- PostgreSQL 16.0+

**Connection:**
- SQLAlchemy 2.0 async engine
- Sessions: `CurrentSession` (auto-commit) or `CurrentSessionTransaction` (with transaction)
- Session factory: `async_db_session` in `backend/database/db.py`

**Models:**
- Base classes: `MappedBase`, `DataClassBase`, `Base` (includes timestamps)
- Mixins: `DateTimeMixin`, `UserMixin`
- Primary keys: `id_key` (autoincrement)
- Always add `from __future__ import annotations` at top of model files with relationships

## Key Systems & Patterns

### Response Patterns

**Location:** `backend/common/response/response_schema.py`

All API responses follow standardized format:
```python
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base

# Without specific schema
@router.get('/', response_model=ResponseModel)
def endpoint():
    return response_base.success(data={'key': 'value'})

# With specific schema
@router.get('/', response_model=ResponseSchemaModel[UserSchema])
def endpoint():
    return ResponseSchemaModel[UserSchema](data=user_obj)

# Fast response (for performance-critical endpoints, bypasses pydantic validation)
def endpoint():
    return response_base.fast_success(data={'key': 'value'})
```

Response structure: `{"code": int, "msg": str, "data": Any}`

### Error Handling

**Location:** `backend/common/exception/errors.py`

Standard exception classes:
- `RequestError` - 400 Bad Request
- `ForbiddenError` - 403 Forbidden
- `NotFoundError` - 404 Not Found
- `AuthorizationError` - 403 Permission Denied
- `TokenError` - 401 Authentication
- `ServerError` - 500 Internal Server Error
- `CustomError` - Custom error codes (use with `CustomErrorCode`)

Usage:
```python
from backend.common.exception.errors import NotFoundError, CustomError

raise NotFoundError(msg='User not found')
raise CustomError(error=CustomErrorCode.SOMETHING_WRONG, data=extra_info)
```

### RBAC & Permissions

**Mode:** Role-Menu (default) or Casbin plugin

**Configuration:** `backend/core/conf.py`
- `RBAC_ROLE_MENU_MODE = True` enables role-menu mode
- `RBAC_ROLE_MENU_EXCLUDE` lists permission codes that bypass RBAC

**Usage:**
```python
from backend.common.security.rbac import DependsRBAC
from backend.common.security.permission import RequestPermission

@router.post(
    '/endpoint',
    dependencies=[
        Depends(RequestPermission('sys:api:add')),  # Format: module:resource:action
        DependsRBAC,
    ],
)
async def protected_endpoint():
    pass
```

Permission codes must match menu permission codes in the database.

### JWT Authentication

**Middleware:** `backend/middleware/jwt_auth_middleware.py`

- Extracts `Authorization: Bearer <token>` header
- Whitelist paths in `backend/core/conf.py`:
  - `TOKEN_REQUEST_PATH_EXCLUDE` - exact paths
  - `TOKEN_REQUEST_PATH_EXCLUDE_PATTERN` - regex patterns
- User info available via `request.user` after authentication

### Internationalization (i18n)

**Language files:** `backend/app/locale/` (JSON or YAML format)

**Naming:** ISO language codes (e.g., `ru-RU.json`, `en-US.json`)

**Default language:** Set in `backend/core/conf.py` → `I18N_DEFAULT_LANGUAGE`

**Dynamic switching:** Reads `Accept-Language` header automatically via `I18nMiddleware`

**Usage:**
```python
from backend.common.i18n import t

message = t('response.success')  # Chained dot notation
error_msg = t('error.captcha.expired')
```

### Pagination

**Location:** `backend/common/pagination.py`

**Dependency injection:**
```python
from backend.common.pagination import DependsPagination, paging_data, PageData
from backend.common.response.response_schema import ResponseSchemaModel

@router.get('/', response_model=ResponseSchemaModel[PageData[UserSchema]])
async def get_users(db: CurrentSession, page: DependsPagination):
    select = ... # Build SQLAlchemy select
    page_data = await paging_data(db, select)
    return ResponseSchemaModel[PageData[UserSchema]](data=page_data)
```

Query parameters: `?page=1&size=20` (size max: 200)

Response includes: `items`, `total`, `page`, `size`, `total_pages`, `links` (first, last, next, prev)

### CRUD Operations

**Library:** `sqlalchemy-crud-plus`

**Naming conventions:**
- `get()` - Fetch single record
- `get_by_xxx()` - Fetch by specific field
- `get_select()` - Build selectable query
- `get_list()` - Fetch list with filters
- `get_all()` - Fetch all records
- `create()` - Create new record
- `update()` - Update existing record
- `delete()` - Delete record

## Coding Standards (from roles.txt)

### Type Annotations
- Use Python 3.10+ syntax
- Annotate all function parameters and return values (except `args`/`kwargs`)
- Explicit types for dicts: `dict[str, Any]`
- Explicit types for lists: `list[dict[str, str]]`

### Documentation
- Always start files with:
  ```python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  ```
- Function docstrings:
  - Multi-line for functions with params
  - Single-line for functions without params
  - Format: `:param name: description` and `:return:` (no description for return)

### Code Style
- Max line length: 120 characters
- Use early returns instead of nested if/else
- Avoid ternary operators when possible
- Use snake_case for variables, PascalCase for classes
- No single-letter variables (except loop counters)

### Async/Sync
- Use `async def` for I/O-bound operations (database, external APIs)
- Use `def` for pure synchronous functions
- Handle blocking operations with `run_in_threadpool`

### Schema & Model Patterns
- Add `Field` to all schema attributes
- Model docstrings: only describe which table it represents
- Schema docstrings: brief description (few words)
- Don't use strings in `relationship` `Mapped[]` types
- Add `from __future__ import annotations` for models with relationships

### Validation & Error Handling
- Use Pydantic models for all validation
- Don't add new field validators arbitrarily
- Use early return pattern for error conditions
- Add try/except only when necessary
- Use custom errors from `backend/common/exception/errors.py`
- Log errors via `backend/common/log.py`

### Performance
- Use Redis for caching: `backend/database/redis.py`
- Use async operations for all database/external calls
- Minimize blocking I/O

## Utility Functions (backend/utils/)

The project provides several utility modules for common operations:

### Timezone Utilities (`backend/utils/timezone.py`)

**Singleton instance:** `timezone`

```python
from backend.utils.timezone import timezone

# Get current time in configured timezone
now = timezone.now()

# Convert datetime to configured timezone
local_time = timezone.from_datetime(some_datetime)

# Convert string to datetime
dt = timezone.from_str('2024-01-01 12:00:00')
dt_custom = timezone.from_str('01/01/2024', '%m/%d/%Y')

# Convert datetime to string
time_str = timezone.to_str(some_datetime)

# Convert to UTC
utc_time = timezone.to_utc(some_datetime)
utc_from_timestamp = timezone.to_utc(1234567890)
```

Timezone configuration: `DATETIME_TIMEZONE` and `DATETIME_FORMAT` in `backend/core/conf.py`

### Serialization (`backend/utils/serializers.py`)

```python
from backend.utils.serializers import (
    select_columns_serialize,
    select_list_serialize,
    select_as_dict,
    MsgSpecJSONResponse
)

# Serialize single SQLAlchemy row (columns only, no relationships)
row_dict = select_columns_serialize(user_row)

# Serialize list of SQLAlchemy rows
users_list = select_list_serialize(user_rows)

# Convert row to dict (includes relationships)
full_dict = select_as_dict(user_row)
with_aliases = select_as_dict(user_row, use_alias=True)

# High-performance JSON response (used internally by fast_success)
return MsgSpecJSONResponse({'key': 'value'})
```

### Tree Building (`backend/utils/build_tree.py`)

```python
from backend.utils.build_tree import get_tree_data, get_vben5_tree_data
from backend.common.enums import BuildTreeType

# Build tree structure from flat data (requires 'id' and 'parent_id' fields)
tree = get_tree_data(
    rows,
    build_type=BuildTreeType.traversal,  # or BuildTreeType.recursive
    is_sort=True,
    sort_key='sort'
)

# Build vben5 frontend menu tree structure
vben_tree = get_vben5_tree_data(rows, is_sort=True, sort_key='sort')
```

**Algorithm choices:**
- `traversal` (default) - Better performance, recommended
- `recursive` - Higher performance impact, use only for small datasets

### Encryption (`backend/utils/encrypt.py`)

```python
from backend.utils.encrypt import AESCipher, Md5Cipher, ItsDCipher

# AES encryption/decryption
aes = AESCipher(key='your_32_byte_hex_key')
encrypted = aes.encrypt('sensitive data')
decrypted = aes.decrypt(encrypted)

# MD5 hashing (one-way)
hash_value = Md5Cipher.encrypt('password123')

# ItsDangerous encryption (handles serialization)
its = ItsDCipher(key='your_32_byte_hex_key')
encrypted = its.encrypt({'user_id': 123, 'role': 'admin'})
decrypted = its.decrypt(encrypted)  # Returns original dict
```

### Request Parsing (`backend/utils/request_parse.py`)

```python
from backend.utils.request_parse import (
    get_request_ip,
    parse_ip_info,
    parse_user_agent_info
)

# Get client IP (handles X-Real-IP and X-Forwarded-For)
ip = get_request_ip(request)

# Parse IP location info (with Redis caching)
ip_info = await parse_ip_info(request)
# Returns: IpInfo(ip=..., country=..., region=..., city=...)

# Parse user agent details
ua_info = parse_user_agent_info(request)
# Returns: UserAgentInfo(user_agent=..., device=..., os=..., browser=...)
```

**IP location modes** (configured in `backend/core/conf.py`):
- `IP_LOCATION_PARSE = 'online'` - High accuracy, calls external API
- `IP_LOCATION_PARSE = 'offline'` - 100% available, uses local database
- `IP_LOCATION_PARSE = 'false'` - Disabled

### Regex Validation (`backend/utils/re_verify.py`)

```python
from backend.utils.re_verify import is_phone, is_git_url, search_string, match_string

# Validate phone number (Chinese format)
if is_phone('13812345678'):
    # Valid phone number
    pass

# Validate git URL
if is_git_url('https://github.com/user/repo.git'):
    # Valid git URL
    pass

# Custom regex operations
result = search_string(r'\d+', 'abc123def')  # Searches anywhere
result = match_string(r'\d+', '123abc')  # Matches from start
```

### Trace ID (`backend/utils/trace_id.py`)

```python
from backend.utils.trace_id import get_request_trace_id

# Get current request trace ID (from context)
trace_id = get_request_trace_id()
```

Trace IDs are automatically generated for each request and stored in context. Configuration in `backend/core/conf.py`:
- `TRACE_ID_REQUEST_HEADER_KEY = 'X-Request-ID'`
- `TRACE_ID_LOG_LENGTH = 32`

### Async to Sync Wrapper (`backend/utils/_await.py`)

```python
from backend.utils._await import run_await

# Wrap async function to make it callable from sync context
@run_await
async def async_operation():
    return await some_async_call()

# Call from sync context
result = async_operation()  # No await needed
```

This is useful when you need to call async functions from synchronous code (like CLI commands).

### Demo Site Protection (`backend/utils/demo_site.py`)

```python
from backend.utils.demo_site import demo_site

# Use as dependency to protect endpoints in demo mode
@router.post('/delete', dependencies=[Depends(demo_site)])
async def delete_item():
    pass
```

When `DEMO_MODE = True` in config, all non-GET/OPTIONS requests are blocked except those in `DEMO_MODE_EXCLUDE`.

## Built-in Plugins

The project includes built-in plugins that extend the admin application with common features.

### Config Plugin (`backend/plugin/config/`)

**Purpose:** System parameter configuration management

**Use case:** Store dynamic system parameters that can be modified at runtime without code changes or redeployment.

**Database table:** `sys_config`

**Key fields:**
- `name` - Configuration display name
- `type` - Configuration type/category (optional)
- `key` - Unique configuration key identifier
- `value` - Configuration value (stored as text)
- `is_frontend` - Boolean flag indicating if config should be exposed to frontend
- `remark` - Optional description

**API endpoints:** `/api/v1/configs`

**Common usage:**
```python
# Store dynamic settings like:
# - Feature flags (enable_notifications: true/false)
# - System limits (max_upload_size: 5242880)
# - External service URLs (payment_api_url: https://...)
# - Display settings (items_per_page: 20)
```

### Dict Plugin (`backend/plugin/dict/`)

**Purpose:** Data dictionary management for constraining frontend data display

**Use case:** Define enumeration values and their display labels used throughout the application (e.g., user status, order types, etc.).

**Database tables:**
- `sys_dict_type` - Dictionary types/categories
- `sys_dict_data` - Dictionary data items (belongs to a type)

**Relationship:** One dict type has many dict data items (one-to-many)

**Dict Type fields:**
- `name` - Dictionary type display name
- `code` - Unique dictionary type code
- `remark` - Optional description

**Dict Data fields:**
- `type_id` / `type_code` - Foreign key to dict type
- `label` - Display label (shown to users)
- `value` - Actual value (used in code)
- `color` - Optional color for frontend display
- `sort` - Sort order
- `status` - Enable/disable flag (0=disabled, 1=enabled)

**API endpoints:**
- `/api/v1/dict-types` - Manage dictionary types
- `/api/v1/dict-datas` - Manage dictionary data

**Common usage:**
```python
# Example: User Status Dictionary
# Type: user_status (code)
# Data items:
#   - label: "Active", value: "1", color: "green"
#   - label: "Inactive", value: "0", color: "gray"
#   - label: "Banned", value: "-1", color: "red"

# Frontend can fetch this dictionary and display appropriate labels/colors
# Backend validates values against the dictionary
```

**Plugin structure:** Both plugins follow the standard app structure:
```
plugin/name/
├── api/           # API endpoints
├── crud/          # Database operations
├── model/         # SQLAlchemy models
├── schema/        # Pydantic schemas
├── service/       # Business logic
├── sql/           # Database initialization scripts
├── plugin.toml    # Plugin metadata
└── README.md      # Plugin documentation
```

Both plugins extend the `admin` app (configured in `plugin.toml`).

## Celery Task System (`backend/app/task/`)

**Purpose:** Distributed asynchronous task processing with database-backed scheduling

### Architecture

**Broker:** RabbitMQ (default) or Redis
**Result Backend:** PostgreSQL
**Scheduler:** Database-backed with 5-second polling, Redis distributed locking

**Task discovery:** Auto-discovers tasks from any `tasks.py` file in `backend/app/task/tasks/` subdirectories

### Creating Tasks

```python
from backend.app.task.celery import celery_app
from celery import shared_task

# Simple task
@celery_app.task(name='my_task')
def my_task(param: str) -> str:
    return 'result'

# Async task (recommended for I/O operations)
@shared_task
async def cleanup_task() -> str:
    async with async_db_session.begin() as db:
        # Database operations
        return 'Success'
```

### Scheduling

**Two schedule types:**
- **Interval**: Every N seconds/minutes/hours/days
- **Crontab**: Unix cron expressions (5 fields: `minute hour day_of_week day_of_month month_of_year`)

**Code-based schedules** (`tasks/beat.py`):
```python
LOCAL_BEAT_SCHEDULE = {
    'Task Name': {
        'task': 'task_name_or_path',
        'schedule': TzAwareCrontab('0', '2', '*', '*', '*'),  # Daily 2 AM
        'args': [],
        'kwargs': {},
    },
}
```

**Database schedules:** Managed via API `/api/v1/schedulers` or directly in `task_scheduler` table

**Dynamic scheduling features:**
- Runtime schedule modifications
- Start time (delay execution)
- Expiration (stop after datetime/seconds)
- One-off tasks (run once then disable)
- Queue routing

### Executing Tasks

```python
# Async execution (returns immediately with task ID)
result = my_task.delay('param')
task_id = result.id

# Check result later
result = celery_app.AsyncResult(task_id)
if result.ready():
    value = result.result
```

### API Endpoints

- `POST /api/v1/schedulers` - Create scheduled task
- `GET /api/v1/schedulers` - List scheduled tasks
- `PUT /api/v1/schedulers/{id}` - Update/enable/disable task
- `DELETE /api/v1/schedulers/{id}` - Delete scheduled task
- `GET /api/v1/results/{task_id}` - Query task result
- `POST /api/v1/control/revoke` - Revoke/terminate task

### Task Base Class

All tasks inherit from `TaskBase` with:
- Auto-retry on SQLAlchemy errors
- Lifecycle hooks: `before_start()`, `on_success()`, `on_failure()`
- Socket.IO notifications for task events

## Important Configuration Files

- **`backend/core/conf.py`** - Global settings (Pydantic Settings from `.env`)
- **`.env`** - Environment-specific configuration (copy from `.env.example`)
- **`backend/database/db.py`** - SQLAlchemy engine and session configuration
- **`pyproject.toml`** - Project dependencies and CLI registration

## Development Workflow for New Features

When adding a new feature to an existing app:

1. Define model in `app/*/model/` (if database changes needed)
2. Define schemas in `app/*/schema/` (request/response validation)
3. Create CRUD operations in `app/*/crud/` (database access)
4. Implement business logic in `app/*/service/` (service layer)
5. Create API routes in `app/*/api/v1/*/` (view layer)
6. Register routes in appropriate `router.py` files

When creating a new app, ensure proper structure:
```
app/new-app/
├── api/
├── crud/
├── model/
├── schema/
└── service/
```

Validate that internal code can reference each other correctly across layers.
