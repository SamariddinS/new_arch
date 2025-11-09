---
title: Permission Factory
---

The Permission Factory provides standardized utilities for creating RBAC permission dependencies, reducing boilerplate code and ensuring consistent permission naming conventions across the application.

## Why Use Permission Factory?

**Problems with manual approach:**
```python
# Manual approach - repetitive and error-prone
@router.get('', dependencies=[
    Depends(RequestPermission('sys:user:get')),
    DependsRBAC,
])

@router.post('', dependencies=[
    Depends(RequestPermission('sys:user:add')),
    DependsRBAC,
])

@router.put('/{pk}', dependencies=[
    Depends(RequestPermission('sys:user:edit')),
    DependsRBAC,
])
```

**Benefits of Permission Factory:**
- ✅ Reduces boilerplate code
- ✅ Ensures consistent permission naming conventions
- ✅ Type-safe and IDE-friendly
- ✅ Easy to refactor and maintain
- ✅ Centralized permission logic

## Approach 1: Permission Factory Class (Recommended)

The `PermissionFactory` class creates reusable permission dependencies for a specific module and resource.

### Basic Usage

```python
from fastapi import APIRouter
from backend.common.security.permission_factory import PermissionFactory
from backend.database.db import CurrentSession

router = APIRouter()

# Create factory for 'sys:user' permissions
user_perms = PermissionFactory('sys', 'user')

@router.get('', summary='Get users', dependencies=user_perms.get())
async def get_users(db: CurrentSession):
    pass

@router.post('', summary='Create user', dependencies=user_perms.add())
async def create_user(db: CurrentSession):
    pass

@router.put('/{pk}', summary='Update user', dependencies=user_perms.edit())
async def update_user(db: CurrentSession, pk: int):
    pass

@router.delete('/{pk}', summary='Delete user', dependencies=user_perms.delete())
async def delete_user(db: CurrentSession, pk: int):
    pass
```

### Custom Actions

For non-CRUD operations, use `custom()`:

```python
role_perms = PermissionFactory('sys', 'role')

@router.put(
    '/{pk}/menus',
    summary='Update role menus',
    dependencies=role_perms.custom('menu:edit')
)
async def update_role_menus(pk: int):
    pass  # Permission: 'sys:role:menu:edit'
```

### Module-Level Factory

Create a module-level factory to share across all routes:

```python
# backend/app/admin/api/v1/sys/user.py
from fastapi import APIRouter
from backend.common.security.permission_factory import PermissionFactory

router = APIRouter()

# Define once at module level
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())
async def get_users():
    pass

@router.get('/{pk}', dependencies=_perms.get())
async def get_user(pk: int):
    pass

@router.post('', dependencies=_perms.add())
async def create_user():
    pass
```

## Approach 2: Factory Function

For one-off permissions, use the `create_permission_dependencies()` function:

```python
from backend.common.security.permission_factory import create_permission_dependencies

@router.get(
    '',
    dependencies=create_permission_dependencies('sys', 'user', 'get')
)
async def get_users():
    pass

@router.post(
    '',
    dependencies=create_permission_dependencies('sys', 'user', 'add')
)
async def create_user():
    pass
```

## Approach 3: Cached Factory (Performance)

For applications with many routes, use cached factories:

```python
from backend.common.security.permission_factory import get_cached_permission_factory

# Cached factory - same instance reused
user_perms = get_cached_permission_factory('sys', 'user')
role_perms = get_cached_permission_factory('sys', 'role')

@router.get('', dependencies=user_perms.get())
async def get_users():
    pass
```

## Permission Naming Convention

All permission codes follow the pattern: **`module:resource:action`**

| Component | Description | Examples |
|-----------|-------------|----------|
| `module` | Application module | `sys`, `log`, `task`, `monitor` |
| `resource` | Resource/entity name (singular) | `user`, `role`, `menu`, `dept` |
| `action` | Operation action | `get`, `add`, `edit`, `del` |

### Standard Actions

| Action | HTTP Method | Description |
|--------|-------------|-------------|
| `get` | GET | Read/retrieve data |
| `add` | POST | Create new data |
| `edit` | PUT/PATCH | Update existing data |
| `del` | DELETE | Delete data |

### Custom Actions

For complex operations, use descriptive custom actions:

```python
# sys:user:password:reset
user_perms.custom('password:reset')

# sys:role:menu:edit
role_perms.custom('menu:edit')

# sys:dept:status:toggle
dept_perms.custom('status:toggle')
```

## Migration Guide

### Before (Manual)

```python
from fastapi import APIRouter, Depends
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()

@router.get(
    '',
    dependencies=[
        Depends(RequestPermission('sys:user:get')),
        DependsRBAC,
    ],
)
async def get_users():
    pass

@router.post(
    '',
    dependencies=[
        Depends(RequestPermission('sys:user:add')),
        DependsRBAC,
    ],
)
async def create_user():
    pass
```

### After (Factory)

```python
from fastapi import APIRouter
from backend.common.security.permission_factory import PermissionFactory

router = APIRouter()
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())
async def get_users():
    pass

@router.post('', dependencies=_perms.add())
async def create_user():
    pass
```

## Best Practices

### 1. Use Module-Level Factories

Define factories at module level to avoid repetition:

```python
# ✅ Good - defined once
_user_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_user_perms.get())
async def get_users():
    pass

@router.get('/{pk}', dependencies=_user_perms.get())
async def get_user(pk: int):
    pass
```

```python
# ❌ Bad - recreated for each route
@router.get('', dependencies=PermissionFactory('sys', 'user').get())
async def get_users():
    pass

@router.get('/{pk}', dependencies=PermissionFactory('sys', 'user').get())
async def get_user(pk: int):
    pass
```

### 2. Group Related Routes

Organize routes by resource and use consistent permissions:

```python
# All user-related routes in one file with shared factory
_perms = PermissionFactory('sys', 'user')

# List/detail use same 'get' permission
@router.get('', dependencies=_perms.get())
async def get_users(): pass

@router.get('/{pk}', dependencies=_perms.get())
async def get_user(pk: int): pass

@router.get('/{pk}/roles', dependencies=_perms.get())
async def get_user_roles(pk: int): pass

# Mutations use different permissions
@router.post('', dependencies=_perms.add())
async def create_user(): pass

@router.put('/{pk}', dependencies=_perms.edit())
async def update_user(pk: int): pass

@router.delete('/{pk}', dependencies=_perms.delete())
async def delete_user(pk: int): pass
```

### 3. Use Descriptive Names for Custom Actions

```python
# ✅ Good - descriptive custom actions
user_perms.custom('password:reset')
user_perms.custom('status:toggle')
user_perms.custom('avatar:upload')

# ❌ Bad - unclear custom actions
user_perms.custom('action1')
user_perms.custom('do')
user_perms.custom('update2')
```

### 4. Document Permission Requirements

Add comments for complex permission logic:

```python
# Only admins and managers should access this endpoint
# Permission: sys:user:export
@router.get('/export', dependencies=_perms.custom('export'))
async def export_users():
    pass
```

### 5. Consistent Naming Across Application

| Module | Resource Examples |
|--------|-------------------|
| `sys` | user, role, menu, dept, plugin |
| `log` | login-log, opera-log |
| `task` | scheduler, result |
| `monitor` | server, redis, online |

## Integration with Database Menus

After adding permission dependencies to routes, create corresponding menu entries:

```sql
-- For user read permission
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('View Users', 'user_list', 2, 'sys:user:get', 1);

-- For user create permission
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('Create User', 'user_add', 2, 'sys:user:add', 1);

-- For user update permission
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('Edit User', 'user_edit', 2, 'sys:user:edit', 1);

-- For user delete permission
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('Delete User', 'user_del', 2, 'sys:user:del', 1);
```

Then assign these menus to appropriate roles via the `sys_role_menu` table.

## Advanced Usage

### Combining with Other Dependencies

```python
from backend.common.pagination import DependsPagination

@router.get(
    '',
    dependencies=[
        *_perms.get(),  # Unpack permission dependencies
        DependsPagination,  # Add pagination
    ]
)
async def get_users_paginated():
    pass
```

### Conditional Permissions

```python
from typing import Annotated
from fastapi import Depends

def get_permissions(is_admin: bool) -> list:
    """Conditionally apply permissions based on context"""
    if is_admin:
        return []  # Admins bypass permission checks
    return _perms.get()

@router.get('', dependencies=Depends(get_permissions))
async def get_users():
    pass
```

### Testing Permissions

```python
import pytest
from backend.common.security.permission_factory import PermissionFactory

def test_user_permissions():
    perms = PermissionFactory('sys', 'user')

    # Verify permission structure
    assert len(perms.get()) == 2
    assert len(perms.add()) == 2

    # Verify permission codes
    get_deps = perms.get()
    # Access the RequestPermission dependency and verify the code
    # (implementation depends on your testing setup)
```

## See Also

- [RBAC Documentation](./RBAC.md) - Role-based access control overview
- [RequestPermission](../../backend/common/security/permission.py) - Core permission class
- [Menu Management](../../backend/app/admin/api/v1/sys/menu.py) - Menu and permission management
