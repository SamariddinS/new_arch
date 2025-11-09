# Permission Factory Implementation - Summary

## What Was Added

A professional, best-practice architectural solution for managing RBAC permissions across your FastAPI application. This implementation adds **default GET permissions** to routes and standardizes permission management.

## 📁 Files Created

### 1. Core Implementation
- **`backend/common/security/permission_factory.py`**
  - `PermissionFactory` class - Factory pattern for creating permission dependencies
  - `create_permission_dependencies()` - Functional approach for one-off permissions
  - `get_cached_permission_factory()` - Cached factories for performance
  - `AutoPermission` - Automatic permission derivation from routes (advanced)

### 2. Documentation
- **`docs/backend/reference/permission-factory.md`**
  - Complete API reference
  - Usage examples for all approaches
  - Migration guide from manual to factory pattern
  - Best practices and advanced usage

- **`docs/backend/guide/implementing-get-permissions.md`**
  - Step-by-step implementation guide
  - Complete SQL migration scripts (PostgreSQL)
  - Resource-by-resource checklist
  - Testing strategies
  - Troubleshooting common issues

- **`docs/backend/guide/permission-factory-cheatsheet.md`**
  - Quick reference for daily use
  - Common patterns and templates
  - SQL query examples
  - Testing snippets

### 3. Examples
- **`backend/app/admin/api/v1/sys/user_refactored_example.py`**
  - Complete refactored user routes
  - Side-by-side comparison with original
  - Demonstrates all permission patterns
  - Includes SQL setup scripts

### 4. Updated Documentation
- **`CLAUDE.md`** - Updated RBAC section with permission factory usage

## 🎯 Key Features

### 1. Standardized Permission Naming
All permissions follow the convention: **`module:resource:action`**

```
sys:user:get      → GET /api/v1/sys/users
sys:user:add      → POST /api/v1/sys/users
sys:role:edit     → PUT /api/v1/sys/roles/{pk}
log:opera-log:del → DELETE /api/v1/log/opera-logs/{pk}
```

### 2. Reduced Boilerplate

**Before (Manual):**
```python
@router.get('', dependencies=[
    Depends(RequestPermission('sys:user:get')),
    DependsRBAC,
])
```

**After (Factory):**
```python
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())
```

### 3. Type-Safe and Maintainable
- Single source of truth for permission codes
- IDE autocomplete support
- Easy refactoring
- Centralized permission logic

### 4. Flexible Usage Patterns

**Standard CRUD:**
```python
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())      # sys:user:get
@router.post('', dependencies=_perms.add())     # sys:user:add
@router.put('/{pk}', dependencies=_perms.edit())   # sys:user:edit
@router.delete('/{pk}', dependencies=_perms.delete())  # sys:user:del
```

**Custom Actions:**
```python
@router.put('/{pk}/password', dependencies=_perms.custom('password:reset'))
# Permission: sys:user:password:reset
```

## 🚀 Quick Start

### Step 1: Update a Route File

```python
# backend/app/admin/api/v1/sys/user.py
from backend.common.security.permission_factory import PermissionFactory

router = APIRouter()
_perms = PermissionFactory('sys', 'user')

# Before: Only JWT auth
@router.get('', dependencies=[DependsJwtAuth])

# After: Permission required
@router.get('', dependencies=_perms.get())
```

### Step 2: Create Database Permissions

```sql
-- Create menu entry for 'sys:user:get' permission
INSERT INTO sys_menu (title, name, type, perms, status)
VALUES ('View Users', 'user_get', 2, 'sys:user:get', 1);

-- Assign to admin, manager, hr roles
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT r.id, m.id
FROM sys_role r
CROSS JOIN sys_menu m
WHERE r.name IN ('admin', 'manager', 'hr')
  AND m.perms = 'sys:user:get';
```

### Step 3: Test

```bash
# Users with permission (admin, manager, hr) → 200 OK
curl -H "Authorization: Bearer <admin_token>" \
  http://localhost:8000/api/v1/sys/users

# Users without permission (user role) → 403 Forbidden
curl -H "Authorization: Bearer <user_token>" \
  http://localhost:8000/api/v1/sys/users
```

## 📊 Implementation Approaches

### Approach 1: Permission Factory Class (Recommended)
Best for resources with multiple CRUD operations.

```python
_user_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_user_perms.get())
@router.post('', dependencies=_user_perms.add())
@router.put('/{pk}', dependencies=_user_perms.edit())
@router.delete('/{pk}', dependencies=_user_perms.delete())
```

### Approach 2: Factory Function
Best for one-off permissions.

```python
from backend.common.security.permission_factory import create_permission_dependencies

@router.get('', dependencies=create_permission_dependencies('sys', 'user', 'get'))
```

### Approach 3: Cached Factory
Best for high-traffic applications.

```python
from backend.common.security.permission_factory import get_cached_permission_factory

_perms = get_cached_permission_factory('sys', 'user')
```

## 🗂️ Migration Checklist

Use this to migrate all resources:

- [ ] **User Resource** (`sys:user`)
  - [ ] Update routes
  - [ ] Create menu: `sys:user:get`
  - [ ] Assign to: admin, manager, hr
  - [ ] Test permissions

- [ ] **Role Resource** (`sys:role`)
  - [ ] Update routes
  - [ ] Create menu: `sys:role:get`
  - [ ] Assign to: admin, manager
  - [ ] Test permissions

- [ ] **Menu Resource** (`sys:menu`)
  - [ ] Update routes
  - [ ] Create menu: `sys:menu:get`
  - [ ] Assign to: admin
  - [ ] Test permissions

- [ ] **Department Resource** (`sys:dept`)
  - [ ] Update routes
  - [ ] Create menu: `sys:dept:get`
  - [ ] Assign to: admin, manager, hr
  - [ ] Test permissions

- [ ] **Login Log Resource** (`log:login-log`)
  - [ ] Update routes
  - [ ] Create menu: `log:login-log:get`
  - [ ] Assign to: admin, manager
  - [ ] Test permissions

- [ ] **Operation Log Resource** (`log:opera-log`)
  - [ ] Update routes
  - [ ] Create menu: `log:opera-log:get`
  - [ ] Assign to: admin, manager
  - [ ] Test permissions

## 📖 Documentation Reference

### Quick Access
- **Cheat Sheet**: `docs/backend/guide/permission-factory-cheatsheet.md`
- **Implementation Guide**: `docs/backend/guide/implementing-get-permissions.md`
- **API Reference**: `docs/backend/reference/permission-factory.md`
- **Example Code**: `backend/app/admin/api/v1/sys/user_refactored_example.py`

### SQL Scripts
Complete migration scripts available in:
- `docs/backend/guide/implementing-get-permissions.md` (Section: "Complete Migration Scripts")

## 🎓 Best Practices

### 1. Module-Level Factory Definition
```python
# ✅ Good - defined once
_perms = PermissionFactory('sys', 'user')

@router.get('', dependencies=_perms.get())
@router.get('/{pk}', dependencies=_perms.get())
```

### 2. Consistent Naming
```python
# ✅ Good - follows convention
PermissionFactory('sys', 'user')      # sys:user:*
PermissionFactory('log', 'opera-log') # log:opera-log:*

# ❌ Bad - inconsistent
PermissionFactory('system', 'users')
PermissionFactory('logs', 'operation')
```

### 3. Use Same Permission for Related Reads
```python
# All user read operations use same permission
@router.get('', dependencies=_perms.get())       # List users
@router.get('/{pk}', dependencies=_perms.get())  # Get user detail
@router.get('/{pk}/roles', dependencies=_perms.get())  # Get user roles
```

### 4. Descriptive Custom Actions
```python
# ✅ Good
_perms.custom('password:reset')
_perms.custom('status:toggle')
_perms.custom('avatar:upload')

# ❌ Bad
_perms.custom('action1')
_perms.custom('do')
```

## 🧪 Testing

### Unit Test Example
```python
def test_user_list_requires_permission(client):
    # Login as user without 'sys:user:get'
    response = client.post('/api/v1/auth/login', json={
        'username': 'regular_user',
        'password': 'password'
    })
    token = response.json()['data']['access_token']

    # Should be denied
    response = client.get(
        '/api/v1/sys/users',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403
```

## 🔧 Troubleshooting

### Always Getting 403?
1. Check menu exists: `SELECT * FROM sys_menu WHERE perms = 'sys:user:get';`
2. Check role assignment: `SELECT r.name, m.perms FROM sys_role r JOIN sys_role_menu rm ON r.id = rm.role_id JOIN sys_menu m ON m.id = rm.menu_id WHERE m.perms = 'sys:user:get';`
3. Check user has role: `SELECT r.name FROM sys_user u JOIN sys_user_role ur ON u.id = ur.user_id JOIN sys_role r ON r.id = ur.role_id WHERE u.username = 'your_username';`

### Import Errors?
Ensure file exists: `backend/common/security/permission_factory.py`

### Permission Code Mismatch?
Verify exact match:
- Route: `_perms.get()` → `'sys:user:get'`
- Database: `sys_menu.perms = 'sys:user:get'`

## 🎯 Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Code Lines** | 4 lines per route | 1 line per route |
| **Consistency** | Manual typing | Enforced convention |
| **Maintainability** | Hard to refactor | Easy to refactor |
| **Readability** | Verbose | Concise |
| **Type Safety** | String literals | Factory methods |
| **Documentation** | Scattered | Centralized |

## 📈 Performance

- **Cached Factories**: O(1) lookup via LRU cache
- **No Runtime Overhead**: Permissions resolved at FastAPI dependency injection
- **Database Optimization**: Ensure indexes on `sys_menu.perms`, `sys_role_menu.role_id`, `sys_role_menu.menu_id`

## 🔐 Security Considerations

1. **Permission codes are case-sensitive**: `sys:user:get` ≠ `sys:user:Get`
2. **Superusers bypass all checks**: Set `is_superuser = true` carefully
3. **Menu status affects permissions**: `status = 0` disables permission
4. **Role status affects access**: `role.status = 0` disables role

## 📞 Next Steps

1. **Review Example**: Check `user_refactored_example.py` for complete implementation
2. **Read Cheat Sheet**: Keep `permission-factory-cheatsheet.md` handy during migration
3. **Run SQL Scripts**: Execute migration scripts from implementation guide
4. **Test Thoroughly**: Use testing strategies from implementation guide
5. **Update Gradually**: Migrate one resource at a time, testing each

## 📚 Additional Resources

- **RBAC Overview**: `docs/backend/reference/RBAC.md`
- **Data Permissions**: `docs/backend/reference/data-permission.md`
- **JWT Auth**: `docs/backend/reference/jwt.md`
- **Main Documentation**: `CLAUDE.md`

---

**Questions or Issues?**
- Check troubleshooting section in implementation guide
- Review example code in `user_refactored_example.py`
- Consult cheat sheet for quick reference

**Ready to implement?** Start with the implementation guide: `docs/backend/guide/implementing-get-permissions.md`
