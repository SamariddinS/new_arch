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
   - For plugins: run scripts from `plugin/sql/`
   - Or use CLI: `fba <path_to_sql_script>`

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
- Primary keys: `id_key` (autoincrement) or `snowflake_id_key` (distributed ID)
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
