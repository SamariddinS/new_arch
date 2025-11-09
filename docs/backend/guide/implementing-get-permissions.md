---
title: Implementing GET Permissions - Step-by-Step Guide
---

This guide shows you how to add GET permissions to all routes in your application using the Permission Factory pattern.

## Overview

By default, GET routes in this application only require JWT authentication (`DependsJwtAuth`), meaning any authenticated user can access them. This guide shows how to restrict GET routes by role using RBAC permissions.

## Step-by-Step Implementation

### Step 1: Install Permission Factory

The permission factory utilities are located at:
- `backend/common/security/permission_factory.py`

This module is already created and ready to use.

### Step 2: Update Route Files

For each route file in your application, follow this pattern:

#### Before (Current Implementation)

```python
# backend/app/admin/api/v1/sys/user.py
from fastapi import APIRouter
from backend.common.security.jwt import DependsJwtAuth

router = APIRouter()

@router.get('', summary='Get users', dependencies=[DependsJwtAuth])
async def get_users():
    pass
```

#### After (With Permissions)

```python
# backend/app/admin/api/v1/sys/user.py
from fastapi import APIRouter
from backend.common.security.permission_factory import PermissionFactory

router = APIRouter()

# Create module-level factory
_perms = PermissionFactory('sys', 'user')

@router.get('', summary='Get users', dependencies=_perms.get())
async def get_users():
    pass
```

### Step 3: Create Menu Entries in Database

For each resource that now requires permissions, create menu entries:

```sql
-- Example for user resource permissions
INSERT INTO sys_menu (title, name, type, perms, status, parent_id, sort)
VALUES
    -- Read permission
    ('View Users', 'user_get', 2, 'sys:user:get', 1, NULL, 1),

    -- Write permissions (if using factory for these too)
    ('Create User', 'user_add', 2, 'sys:user:add', 1, NULL, 2),
    ('Edit User', 'user_edit', 2, 'sys:user:edit', 1, NULL, 3),
    ('Delete User', 'user_del', 2, 'sys:user:del', 1, NULL, 4);
```

**Menu field explanation:**
- `type = 2`: Button/permission (not a visible menu item)
- `perms`: Permission code that matches your route
- `status = 1`: Enabled
- `parent_id`: NULL or parent menu ID
- `sort`: Display order

### Step 4: Assign Permissions to Roles

Assign the menu permissions to specific roles:

```sql
-- Assign 'sys:user:get' to admin, manager, and hr roles

-- Method 1: Manual assignment
INSERT INTO sys_role_menu (role_id, menu_id)
VALUES
    (1, 123),  -- admin role, user_get menu
    (2, 123),  -- manager role, user_get menu
    (3, 123);  -- hr role, user_get menu

-- Method 2: Automatic assignment based on role names
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name IN ('admin', 'manager', 'hr')
  AND m.perms = 'sys:user:get';
```

### Step 5: Test Permissions

1. **Login as different roles**:
   - Admin → Should have access
   - Manager → Should have access
   - HR → Should have access
   - User (without permission) → Should get 403 Forbidden

2. **Test the endpoint**:
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/sys/users
   ```

3. **Expected responses**:
   - With permission: 200 OK with data
   - Without permission: 403 Forbidden with error message

## Complete Migration Scripts

### For PostgreSQL

```sql
-- ==========================================
-- Complete GET Permission Setup
-- ==========================================

-- 1. Create permission menu entries for all main resources
INSERT INTO sys_menu (title, name, type, perms, status, sort) VALUES
    -- User permissions
    ('View Users', 'perm_user_get', 2, 'sys:user:get', 1, 10),

    -- Role permissions
    ('View Roles', 'perm_role_get', 2, 'sys:role:get', 1, 20),

    -- Menu permissions
    ('View Menus', 'perm_menu_get', 2, 'sys:menu:get', 1, 30),

    -- Department permissions
    ('View Departments', 'perm_dept_get', 2, 'sys:dept:get', 1, 40),

    -- Data scope permissions
    ('View Data Scopes', 'perm_data_scope_get', 2, 'sys:data-scope:get', 1, 50),

    -- Data rule permissions
    ('View Data Rules', 'perm_data_rule_get', 2, 'sys:data-rule:get', 1, 60),

    -- Login log permissions
    ('View Login Logs', 'perm_login_log_get', 2, 'log:login-log:get', 1, 70),

    -- Operation log permissions
    ('View Operation Logs', 'perm_opera_log_get', 2, 'log:opera-log:get', 1, 80),

    -- Task scheduler permissions
    ('View Task Schedulers', 'perm_scheduler_get', 2, 'task:scheduler:get', 1, 90),

    -- Task result permissions
    ('View Task Results', 'perm_result_get', 2, 'task:result:get', 1, 100);

-- 2. Assign GET permissions to admin role (full access)
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name = 'admin'
  AND m.perms LIKE '%:get';

-- 3. Assign specific GET permissions to manager role
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name = 'manager'
  AND m.perms IN (
    'sys:user:get',
    'sys:role:get',
    'sys:dept:get',
    'log:login-log:get',
    'log:opera-log:get'
  );

-- 4. Assign limited GET permissions to hr role
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name = 'hr'
  AND m.perms IN (
    'sys:user:get',
    'sys:dept:get',
    'log:login-log:get'
  );

-- 5. Verify assignments
SELECT
    r.name AS role_name,
    m.title AS permission_title,
    m.perms AS permission_code
FROM sys_role r
JOIN sys_role_menu rm ON r.id = rm.role_id
JOIN sys_menu m ON m.id = rm.menu_id
WHERE m.perms LIKE '%:get'
ORDER BY r.name, m.perms;
```

### Rollback Script (If Needed)

```sql
-- Remove GET permissions
DELETE FROM sys_role_menu
WHERE menu_id IN (
    SELECT id FROM sys_menu
    WHERE perms LIKE '%:get'
);

-- Remove GET permission menu entries
DELETE FROM sys_menu
WHERE perms LIKE '%:get';
```

## Resource-by-Resource Checklist

Use this checklist to migrate each resource:

### ✅ User Resource (`sys:user`)

- [ ] Update `backend/app/admin/api/v1/sys/user.py`
  - [ ] Add `_perms = PermissionFactory('sys', 'user')`
  - [ ] Change GET routes to use `_perms.get()`
  - [ ] Change POST routes to use `_perms.add()` (if applicable)
  - [ ] Change PUT routes to use `_perms.edit()` (if applicable)
  - [ ] Change DELETE routes to use `_perms.delete()` (if applicable)
- [ ] Create menu entry: `sys:user:get`
- [ ] Assign to roles: admin, manager, hr
- [ ] Test with different roles

### ✅ Role Resource (`sys:role`)

- [ ] Update `backend/app/admin/api/v1/sys/role.py`
- [ ] Create menu entry: `sys:role:get`
- [ ] Assign to roles: admin, manager
- [ ] Test with different roles

### ✅ Menu Resource (`sys:menu`)

- [ ] Update `backend/app/admin/api/v1/sys/menu.py`
- [ ] Create menu entry: `sys:menu:get`
- [ ] Assign to roles: admin
- [ ] Test with different roles

### ✅ Department Resource (`sys:dept`)

- [ ] Update `backend/app/admin/api/v1/sys/dept.py`
- [ ] Create menu entry: `sys:dept:get`
- [ ] Assign to roles: admin, manager, hr
- [ ] Test with different roles

### ✅ Data Scope Resource (`sys:data-scope`)

- [ ] Update `backend/app/admin/api/v1/sys/data_scope.py`
- [ ] Create menu entry: `sys:data-scope:get`
- [ ] Assign to roles: admin
- [ ] Test with different roles

### ✅ Login Log Resource (`log:login-log`)

- [ ] Update `backend/app/admin/api/v1/log/login_log.py`
- [ ] Create menu entry: `log:login-log:get`
- [ ] Assign to roles: admin, manager
- [ ] Test with different roles

### ✅ Operation Log Resource (`log:opera-log`)

- [ ] Update `backend/app/admin/api/v1/log/opera_log.py`
- [ ] Create menu entry: `log:opera-log:get`
- [ ] Assign to roles: admin, manager
- [ ] Test with different roles

## Testing Strategy

### Unit Tests

```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_users_without_permission():
    """Test that users without permission get 403"""
    # Login as user without 'sys:user:get' permission
    response = client.post('/api/v1/auth/login', json={
        'username': 'regular_user',
        'password': 'password123'
    })
    token = response.json()['data']['access_token']

    # Try to access protected endpoint
    response = client.get(
        '/api/v1/sys/users',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 403
    assert 'authorization' in response.json()['msg'].lower()


def test_get_users_with_permission():
    """Test that users with permission can access"""
    # Login as admin (has 'sys:user:get' permission)
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.json()['data']['access_token']

    # Access protected endpoint
    response = client.get(
        '/api/v1/sys/users',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert 'data' in response.json()
```

### Manual Testing Checklist

- [ ] Test admin role → should access all GET endpoints
- [ ] Test manager role → should access assigned GET endpoints
- [ ] Test hr role → should access assigned GET endpoints
- [ ] Test user role → should be denied (403 Forbidden)
- [ ] Test unauthenticated → should be denied (401 Unauthorized)
- [ ] Test with expired token → should be denied (401 Unauthorized)

## Common Issues and Solutions

### Issue 1: All requests return 403 even for admin

**Cause**: Menu permissions not assigned to admin role or menu status disabled

**Solution**:
```sql
-- Check if permission exists
SELECT * FROM sys_menu WHERE perms = 'sys:user:get';

-- Check if assigned to admin role
SELECT r.name, m.perms
FROM sys_role r
JOIN sys_role_menu rm ON r.id = rm.role_id
JOIN sys_menu m ON m.id = rm.menu_id
WHERE r.name = 'admin' AND m.perms = 'sys:user:get';

-- Assign if missing
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r, sys_menu m
WHERE r.name = 'admin' AND m.perms = 'sys:user:get';
```

### Issue 2: Permission code mismatch

**Cause**: Permission code in route doesn't match database

**Solution**: Ensure exact match between:
- Route: `_perms.get()` → generates `sys:user:get`
- Database: `sys_menu.perms = 'sys:user:get'`

### Issue 3: Superuser still gets 403

**Cause**: RBAC verification checks happen before superuser bypass

**Solution**: Ensure `is_superuser = true` in user table:
```sql
UPDATE sys_user SET is_superuser = true WHERE username = 'admin';
```

### Issue 4: Permission factory not found

**Cause**: Import error or module not created

**Solution**:
```python
# Ensure correct import
from backend.common.security.permission_factory import PermissionFactory

# Verify file exists
# backend/common/security/permission_factory.py
```

## Performance Considerations

### Caching

Permission checks are performed on every request. Consider caching:

```python
# Use cached factory for better performance
from backend.common.security.permission_factory import get_cached_permission_factory

_perms = get_cached_permission_factory('sys', 'user')
```

### Database Optimization

Ensure indexes exist:

```sql
-- Index on menu perms for faster lookups
CREATE INDEX IF NOT EXISTS idx_sys_menu_perms ON sys_menu(perms);

-- Index on role_menu relationships
CREATE INDEX IF NOT EXISTS idx_sys_role_menu_role ON sys_role_menu(role_id);
CREATE INDEX IF NOT EXISTS idx_sys_role_menu_menu ON sys_role_menu(menu_id);
```

## Next Steps

After implementing GET permissions:

1. **Document permissions** - Add comments in code explaining which roles need each permission
2. **Update API documentation** - Add permission requirements to OpenAPI/Swagger docs
3. **Create admin UI** - Build interface for admins to manage role-permission assignments
4. **Audit logging** - Log permission denials for security monitoring
5. **Regular review** - Periodically review and update role permissions

## See Also

- [Permission Factory Reference](../reference/permission-factory.md) - Detailed API documentation
- [RBAC Overview](../reference/RBAC.md) - Role-based access control system
- [User Routes Example](../../backend/app/admin/api/v1/sys/user_refactored_example.py) - Complete refactored example
