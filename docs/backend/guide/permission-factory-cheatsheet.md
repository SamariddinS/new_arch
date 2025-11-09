---
title: Permission Factory Quick Reference
---

## Import

```python
from backend.common.security.permission_factory import PermissionFactory
```

## Basic Usage

```python
# Define once at module level
_perms = PermissionFactory('sys', 'user')

# Use in routes
@router.get('', dependencies=_perms.get())
@router.post('', dependencies=_perms.add())
@router.put('/{pk}', dependencies=_perms.edit())
@router.delete('/{pk}', dependencies=_perms.delete())
```

## Permission Code Format

```
module:resource:action

Examples:
  sys:user:get
  sys:role:add
  log:login-log:del
  task:scheduler:edit
```

## Standard Actions

| Method | Factory | Permission Code | Description |
|--------|---------|-----------------|-------------|
| GET | `_perms.get()` | `sys:user:get` | Read/retrieve |
| POST | `_perms.add()` | `sys:user:add` | Create |
| PUT/PATCH | `_perms.edit()` | `sys:user:edit` | Update |
| DELETE | `_perms.delete()` | `sys:user:del` | Delete |

## Custom Actions

```python
# Custom permission for password reset
@router.put('/{pk}/password', dependencies=_perms.custom('password:reset'))
# Permission: sys:user:password:reset

# Custom permission for menu assignment
@router.put('/{pk}/menus', dependencies=_perms.custom('menu:edit'))
# Permission: sys:role:menu:edit
```

## Common Modules & Resources

| Module | Resources |
|--------|-----------|
| `sys` | user, role, menu, dept, plugin, data-scope, data-rule |
| `log` | login-log, opera-log |
| `task` | scheduler, result |
| `monitor` | server, redis, online |

## Combining with Other Dependencies

```python
from backend.common.pagination import DependsPagination

@router.get(
    '',
    dependencies=[
        *_perms.get(),     # Unpack permission dependencies
        DependsPagination,  # Add other dependencies
    ]
)
```

## SQL Templates

### Create Menu Entry

```sql
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('View Users', 'user_get', 2, 'sys:user:get', 1);
```

### Assign to Role

```sql
-- Method 1: Direct assignment
INSERT INTO sys_role_menu (role_id, menu_id)
VALUES (1, 123);  -- role_id=1 (admin), menu_id=123

-- Method 2: By role name
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name = 'admin'
  AND m.perms = 'sys:user:get';
```

### Check Permissions

```sql
-- View all role permissions
SELECT r.name, m.perms
FROM sys_role r
JOIN sys_role_menu rm ON r.id = rm.role_id
JOIN sys_menu m ON m.id = rm.menu_id
ORDER BY r.name, m.perms;

-- Check specific role
SELECT m.perms
FROM sys_role r
JOIN sys_role_menu rm ON r.id = rm.role_id
JOIN sys_menu m ON m.id = rm.menu_id
WHERE r.name = 'manager';
```

## Migration Pattern

### Before

```python
from fastapi import Depends
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

@router.get('', dependencies=[DependsJwtAuth])
async def get_items(): pass

@router.delete('/{pk}', dependencies=[
    Depends(RequestPermission('sys:item:del')),
    DependsRBAC,
])
async def delete_item(pk: int): pass
```

### After

```python
from backend.common.security.permission_factory import PermissionFactory

_perms = PermissionFactory('sys', 'item')

@router.get('', dependencies=_perms.get())
async def get_items(): pass

@router.delete('/{pk}', dependencies=_perms.delete())
async def delete_item(pk: int): pass
```

## Testing

```python
import pytest
from fastapi.testclient import TestClient

def test_permission_denied():
    response = client.get(
        '/api/v1/sys/users',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403

def test_permission_granted():
    response = client.get(
        '/api/v1/sys/users',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
```

## Common Patterns

### Pattern 1: Same Permission for List + Detail

```python
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())
async def list_users(): pass

@router.get('/{pk}', dependencies=_perms.get())
async def get_user(pk: int): pass
```

### Pattern 2: Different Permissions for Sub-resources

```python
_user_perms = PermissionFactory('sys', 'user')
_role_perms = PermissionFactory('sys', 'role')

@router.get('/users', dependencies=_user_perms.get())
async def get_users(): pass

@router.get('/users/{pk}/roles', dependencies=_role_perms.get())
async def get_user_roles(pk: int): pass
```

### Pattern 3: Public + Protected Routes

```python
from backend.common.security.jwt import DependsJwtAuth

_perms = PermissionFactory('sys', 'user')

# Public route - only authentication
@router.get('/me', dependencies=[DependsJwtAuth])
async def get_current_user(): pass

# Protected route - requires permission
@router.get('', dependencies=_perms.get())
async def get_all_users(): pass
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Always 403 | Check menu exists and assigned to role |
| Import error | Verify file path: `backend/common/security/permission_factory.py` |
| Wrong permission | Verify menu `perms` matches factory code |
| Superuser denied | Set `is_superuser = true` in database |

## Performance Tips

```python
# Use cached factory for high-traffic apps
from backend.common.security.permission_factory import get_cached_permission_factory

_perms = get_cached_permission_factory('sys', 'user')
```

## Complete Example

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated
from fastapi import APIRouter, Path
from backend.common.security.permission_factory import PermissionFactory
from backend.common.pagination import DependsPagination
from backend.database.db import CurrentSession

router = APIRouter()
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=[*_perms.get(), DependsPagination])
async def get_users(db: CurrentSession):
    """Get paginated users - requires 'sys:user:get' permission"""
    pass

@router.get('/{pk}', dependencies=_perms.get())
async def get_user(db: CurrentSession, pk: Annotated[int, Path()]):
    """Get single user - requires 'sys:user:get' permission"""
    pass

@router.post('', dependencies=_perms.add())
async def create_user(db: CurrentSession):
    """Create user - requires 'sys:user:add' permission"""
    pass

@router.put('/{pk}', dependencies=_perms.edit())
async def update_user(db: CurrentSession, pk: int):
    """Update user - requires 'sys:user:edit' permission"""
    pass

@router.delete('/{pk}', dependencies=_perms.delete())
async def delete_user(db: CurrentSession, pk: int):
    """Delete user - requires 'sys:user:del' permission"""
    pass
```

---

**See Full Documentation:**
- [Permission Factory Reference](../reference/permission-factory.md)
- [Implementation Guide](./implementing-get-permissions.md)
- [RBAC Overview](../reference/RBAC.md)
