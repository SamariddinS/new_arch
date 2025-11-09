#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Permission factory utilities for standardized RBAC permission dependencies

This module provides factory functions and utilities for creating consistent
permission dependencies across the application, reducing boilerplate code and
ensuring permission naming conventions are followed.
"""
from functools import lru_cache
from typing import Literal

from fastapi import Depends, Request

from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

# Type alias for CRUD actions
CrudAction = Literal['get', 'add', 'edit', 'del']


class PermissionFactory:
    """
    Factory class for creating standardized permission dependencies

    This class provides methods to generate permission dependencies following
    the convention: module:resource:action (e.g., 'sys:user:get')
    """

    def __init__(self, module: str, resource: str) -> None:
        """
        Initialize permission factory for a specific module and resource

        :param module: Module name (e.g., 'sys', 'task', 'log')
        :param resource: Resource name (e.g., 'user', 'role', 'menu')
        """
        self.module = module
        self.resource = resource

    def _build_permission(self, action: str) -> str:
        """
        Build permission code from module, resource, and action

        :param action: Action name (e.g., 'get', 'add', 'edit', 'del')
        :return: Permission code (e.g., 'sys:user:get')
        """
        return f'{self.module}:{self.resource}:{action}'

    def get(self) -> list:
        """
        Generate GET permission dependencies

        :return: List of dependencies for GET operations
        """
        return [
            Depends(RequestPermission(self._build_permission('get'))),
            DependsRBAC,
        ]

    def add(self) -> list:
        """
        Generate ADD (CREATE) permission dependencies

        :return: List of dependencies for CREATE operations
        """
        return [
            Depends(RequestPermission(self._build_permission('add'))),
            DependsRBAC,
        ]

    def edit(self) -> list:
        """
        Generate EDIT (UPDATE) permission dependencies

        :return: List of dependencies for UPDATE operations
        """
        return [
            Depends(RequestPermission(self._build_permission('edit'))),
            DependsRBAC,
        ]

    def delete(self) -> list:
        """
        Generate DELETE permission dependencies

        :return: List of dependencies for DELETE operations
        """
        return [
            Depends(RequestPermission(self._build_permission('del'))),
            DependsRBAC,
        ]

    def custom(self, action: str) -> list:
        """
        Generate custom permission dependencies

        :param action: Custom action name
        :return: List of dependencies for custom operations
        """
        return [
            Depends(RequestPermission(self._build_permission(action))),
            DependsRBAC,
        ]

    def all_crud(self) -> dict[str, list]:
        """
        Generate all CRUD permission dependencies

        :return: Dictionary mapping action names to their dependencies
        """
        return {
            'get': self.get(),
            'add': self.add(),
            'edit': self.edit(),
            'del': self.delete(),
        }


def create_permission_dependencies(
    module: str,
    resource: str,
    action: CrudAction | str,
) -> list:
    """
    Create permission dependencies using module:resource:action convention

    Usage:
        @router.get('', dependencies=create_permission_dependencies('sys', 'user', 'get'))
        async def get_users():
            pass

    :param module: Module name (e.g., 'sys', 'task')
    :param resource: Resource name (e.g., 'user', 'role')
    :param action: Action name (e.g., 'get', 'add', 'edit', 'del')
    :return: List of permission dependencies
    """
    permission_code = f'{module}:{resource}:{action}'
    return [
        Depends(RequestPermission(permission_code)),
        DependsRBAC,
    ]


@lru_cache(maxsize=128)
def get_cached_permission_factory(module: str, resource: str) -> PermissionFactory:
    """
    Get or create a cached permission factory instance

    Caching ensures the same factory is reused for the same module:resource pair,
    improving performance in applications with many routes.

    :param module: Module name
    :param resource: Resource name
    :return: Cached PermissionFactory instance
    """
    return PermissionFactory(module, resource)


class AutoPermission:
    """
    Automatic permission resolver based on request path and method

    This class automatically derives permission codes from the request path,
    following the convention that paths like '/api/v1/sys/users' should check
    for 'sys:user:get' permission on GET requests.
    """

    # HTTP method to action mapping
    METHOD_ACTION_MAP = {
        'GET': 'get',
        'POST': 'add',
        'PUT': 'edit',
        'PATCH': 'edit',
        'DELETE': 'del',
    }

    @classmethod
    def from_path(cls, path: str, method: str) -> str | None:
        """
        Derive permission code from request path and HTTP method

        Examples:
            - Path: '/api/v1/sys/users', Method: 'GET' -> 'sys:user:get'
            - Path: '/api/v1/sys/roles', Method: 'POST' -> 'sys:role:add'
            - Path: '/api/v1/log/opera-logs', Method: 'DELETE' -> 'log:opera-log:del'

        :param path: Request path
        :param method: HTTP method
        :return: Derived permission code or None if cannot derive
        """
        # Remove trailing slash and split path
        path = path.rstrip('/')
        parts = [p for p in path.split('/') if p]

        # Expected format: ['api', 'v1', 'module', 'resource']
        if len(parts) < 4 or parts[0] != 'api':
            return None

        # Extract module and resource
        module = parts[2]  # e.g., 'sys', 'log', 'task'
        resource = parts[3]  # e.g., 'users', 'roles', 'menus'

        # Convert plural resource to singular (users -> user)
        if resource.endswith('s') and not resource.endswith('ss'):
            resource = resource[:-1]

        # Convert kebab-case to singular form (opera-logs -> opera-log)
        resource = resource.replace('_', '-')

        # Get action from HTTP method
        action = cls.METHOD_ACTION_MAP.get(method.upper())
        if not action:
            return None

        return f'{module}:{resource}:{action}'

    def __init__(self, derive_from_path: bool = True) -> None:
        """
        Initialize auto permission resolver

        :param derive_from_path: Whether to auto-derive permission from path
        """
        self.derive_from_path = derive_from_path

    async def __call__(self, request: Request) -> str | None:
        """
        Callable to be used as FastAPI dependency

        :param request: FastAPI request object
        :return: Derived permission code or None
        """
        if not self.derive_from_path:
            return None

        return self.from_path(request.url.path, request.method)
