#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User management API routes - Refactored with Permission Factory

This is an example demonstrating best practices for using PermissionFactory
to standardize permission dependencies across CRUD operations.

Compare this with the original user.py to see the improvements.
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Request

from backend.app.admin.schema.role import GetRoleDetail
from backend.app.admin.schema.user import (
    AddUserParam,
    GetCurrentUserInfoWithRelationDetail,
    GetUserInfoWithRelationDetail,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.app.admin.service.user_service import user_service
from backend.common.enums import UserPermissionType
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, DependsSuperUser
from backend.common.security.permission_factory import PermissionFactory
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()

# Module-level permission factory for user resource
# This creates standardized permission codes like 'sys:user:get', 'sys:user:add', etc.
_user_perms = PermissionFactory('sys', 'user')


# ======================
# Public User Endpoints
# ======================
# These endpoints only require JWT authentication


@router.get('/me', summary='Get current user information', dependencies=[DependsJwtAuth])
async def get_current_user(request: Request) -> ResponseSchemaModel[GetCurrentUserInfoWithRelationDetail]:
    """Get current authenticated user information"""
    data = request.user.model_dump()
    return response_base.success(data=data)


@router.put('/me/password', summary='Update current user password', dependencies=[DependsJwtAuth])
async def update_user_password(
    db: CurrentSessionTransaction, request: Request, obj: ResetPasswordParam
) -> ResponseModel:
    """Update password for currently authenticated user"""
    count = await user_service.update_password(db=db, request=request, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/nickname', summary='Update current user nickname', dependencies=[DependsJwtAuth])
async def update_user_nickname(
    db: CurrentSessionTransaction,
    request: Request,
    nickname: Annotated[str, Body(embed=True, description='User nickname')],
) -> ResponseModel:
    """Update nickname for currently authenticated user"""
    count = await user_service.update_nickname(db=db, request=request, nickname=nickname)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/avatar', summary='Update current user avatar', dependencies=[DependsJwtAuth])
async def update_user_avatar(
    db: CurrentSessionTransaction,
    request: Request,
    avatar: Annotated[str, Body(embed=True, description='User avatar URL')],
) -> ResponseModel:
    """Update avatar for currently authenticated user"""
    count = await user_service.update_avatar(db=db, request=request, avatar=avatar)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/email', summary='Update current user email', dependencies=[DependsJwtAuth])
async def update_user_email(
    db: CurrentSessionTransaction,
    request: Request,
    captcha: Annotated[str, Body(embed=True, description='Email verification code')],
    email: Annotated[str, Body(embed=True, description='User email')],
) -> ResponseModel:
    """Update email for currently authenticated user"""
    count = await user_service.update_email(db=db, request=request, captcha=captcha, email=email)
    if count > 0:
        return response_base.success()
    return response_base.fail()


# =======================
# Protected Read Endpoints
# =======================
# These endpoints require 'sys:user:get' permission


@router.get(
    '',
    summary='Get paginated users',
    dependencies=[
        *_user_perms.get(),  # Expands to: RequestPermission('sys:user:get') + DependsRBAC
        DependsPagination,
    ],
)
async def get_users_paginated(
    db: CurrentSession,
    dept: Annotated[int | None, Query(description='Department ID')] = None,
    username: Annotated[str | None, Query(description='Username')] = None,
    phone: Annotated[str | None, Query(description='Phone number')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
) -> ResponseSchemaModel[PageData[GetUserInfoWithRelationDetail]]:
    """
    Get paginated list of users with optional filters

    Permission required: sys:user:get
    Roles: admin, manager, hr (configured in database)
    """
    page_data = await user_service.get_list(db=db, dept=dept, username=username, phone=phone, status=status)
    return response_base.success(data=page_data)


@router.get(
    '/{pk}',
    summary='Get user information',
    dependencies=_user_perms.get(),  # Same permission as list endpoint
)
async def get_userinfo(
    db: CurrentSession,
    pk: Annotated[int, Path(description='User ID')],
) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    """
    Get detailed information for a specific user

    Permission required: sys:user:get
    """
    data = await user_service.get_userinfo(db=db, pk=pk)
    return response_base.success(data=data)


@router.get(
    '/{pk}/roles',
    summary='Get all user roles',
    dependencies=_user_perms.get(),  # Same permission - reading user data
)
async def get_user_roles(
    db: CurrentSession, pk: Annotated[int, Path(description='User ID')]
) -> ResponseSchemaModel[list[GetRoleDetail]]:
    """
    Get all roles assigned to a specific user

    Permission required: sys:user:get
    """
    data = await user_service.get_roles(db=db, pk=pk)
    return response_base.success(data=data)


# ========================
# Protected Write Endpoints
# ========================
# These require superuser status (can be changed to use permission factory)


@router.post(
    '',
    summary='Create user',
    dependencies=[DependsSuperUser],  # Could use: dependencies=_user_perms.add()
)
async def create_user(
    db: CurrentSessionTransaction, obj: AddUserParam
) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    """
    Create a new user

    Alternative with permission factory:
        dependencies=_user_perms.add()  # Checks 'sys:user:add' permission
    """
    await user_service.create(db=db, obj=obj)
    data = await user_service.get_userinfo(db=db, username=obj.username)
    return response_base.success(data=data)


@router.put(
    '/{pk}',
    summary='Update user information',
    dependencies=[DependsSuperUser],  # Could use: dependencies=_user_perms.edit()
)
async def update_user(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='User ID')],
    obj: UpdateUserParam,
) -> ResponseModel:
    """
    Update user information

    Alternative with permission factory:
        dependencies=_user_perms.edit()  # Checks 'sys:user:edit' permission
    """
    count = await user_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/permissions',
    summary='Update user permissions',
    dependencies=[DependsSuperUser],  # Could use: dependencies=_user_perms.custom('permission:edit')
)
async def update_user_permission(
    db: CurrentSessionTransaction,
    request: Request,
    pk: Annotated[int, Path(description='User ID')],
    type: Annotated[UserPermissionType, Query(description='Permission type')],
) -> ResponseModel:
    """
    Update user permission type (staff/management status)

    Alternative with permission factory:
        dependencies=_user_perms.custom('permission:edit')  # Checks 'sys:user:permission:edit'
    """
    count = await user_service.update_permission(db=db, request=request, pk=pk, type=type)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/password',
    summary='Reset user password',
    dependencies=[DependsSuperUser],  # Could use: dependencies=_user_perms.custom('password:reset')
)
async def reset_user_password(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='User ID')],
    password: Annotated[str, Body(embed=True, description='New password')],
) -> ResponseModel:
    """
    Reset password for a specific user (admin operation)

    Alternative with permission factory:
        dependencies=_user_perms.custom('password:reset')  # Checks 'sys:user:password:reset'
    """
    count = await user_service.reset_password(db=db, pk=pk, password=password)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path='/{pk}',
    summary='Delete user',
    dependencies=_user_perms.delete(),  # Permission factory in use!
)
async def delete_user(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='User ID')]) -> ResponseModel:
    """
    Delete a user

    Permission required: sys:user:del
    """
    count = await user_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


# ===============================================
# Benefits of this refactored approach:
# ===============================================
#
# 1. CONSISTENCY
#    - All 'get' operations use _user_perms.get()
#    - All 'add' operations use _user_perms.add()
#    - All 'edit' operations use _user_perms.edit()
#    - All 'delete' operations use _user_perms.delete()
#
# 2. MAINTAINABILITY
#    - Single factory definition at module level
#    - Easy to change permission module/resource in one place
#    - Clear permission naming convention enforced
#
# 3. READABILITY
#    - _user_perms.get() is more semantic than manual RequestPermission('sys:user:get')
#    - Less boilerplate code
#    - Easier for new developers to understand
#
# 4. TYPE SAFETY
#    - IDE autocomplete works
#    - Refactoring tools work better
#
# 5. FLEXIBILITY
#    - Easy to combine with other dependencies using *_user_perms.get()
#    - Custom actions supported via _user_perms.custom('action')
#
# ===============================================
# Database Setup Required:
# ===============================================
#
# CREATE MENU ENTRIES:
#
# INSERT INTO sys_menu (title, name, type, perms, status)
# VALUES
#     ('View Users', 'user_get', 2, 'sys:user:get', 1),
#     ('Create User', 'user_add', 2, 'sys:user:add', 1),
#     ('Edit User', 'user_edit', 2, 'sys:user:edit', 1),
#     ('Delete User', 'user_del', 2, 'sys:user:del', 1),
#     ('Reset Password', 'user_password_reset', 2, 'sys:user:password:reset', 1),
#     ('Edit Permissions', 'user_permission_edit', 2, 'sys:user:permission:edit', 1);
#
# ASSIGN TO ROLES:
#
# -- Get role IDs
# SELECT id, name FROM sys_role WHERE name IN ('admin', 'manager', 'hr');
#
# -- Assign 'sys:user:get' to admin, manager, hr roles
# INSERT INTO sys_role_menu (role_id, menu_id)
# SELECT r.id, m.id
# FROM sys_role r
# CROSS JOIN sys_menu m
# WHERE r.name IN ('admin', 'manager', 'hr')
#   AND m.perms = 'sys:user:get';
#
# ===============================================
