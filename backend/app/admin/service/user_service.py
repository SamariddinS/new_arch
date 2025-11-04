import random

from collections.abc import Sequence
from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import Role, User
from backend.app.admin.schema.user import (
    AddUserParam,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.common.context import ctx
from backend.common.enums import UserPermissionType
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.common.response.response_code import CustomErrorCode
from backend.common.security.jwt import get_token, jwt_decode, password_verify
from backend.core.conf import settings
from backend.database.redis import redis_client


class UserService:
    """User service class"""

    @staticmethod
    async def get_userinfo(*, db: AsyncSession, pk: int | None = None, username: str | None = None) -> User:
        """
        Get user information

        :param db: Database session
        :param pk: User ID
        :param username: Username
        :return:
        """
        user = await user_dao.get_with_relation(db, user_id=pk, username=username)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        return user

    @staticmethod
    async def get_roles(*, db: AsyncSession, pk: int) -> Sequence[Role]:
        """
        Get all user roles

        :param db: Database session
        :param pk: User ID
        :return:
        """
        user = await user_dao.get_with_relation(db, user_id=pk)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        return user.roles

    @staticmethod
    async def get_list(*, db: AsyncSession, dept: int, username: str, phone: str, status: int) -> dict[str, Any]:
        """
        Get user list

        :param db: Database session
        :param dept: Department ID
        :param username: Username
        :param phone: Phone number
        :param status: Status
        :return:
        """
        user_select = await user_dao.get_select(dept=dept, username=username, phone=phone, status=status)
        return await paging_data(db, user_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: AddUserParam) -> None:
        """
        Create user

        :param db: Database session
        :param obj: Add user parameters
        :return:
        """
        if await user_dao.get_by_username(db, obj.username):
            raise errors.ConflictError(msg='Username already registered')
        obj.nickname = obj.nickname or f'#{random.randrange(88888, 99999)}'
        if not obj.password:
            raise errors.RequestError(msg='Password cannot be empty')
        if not await dept_dao.get(db, obj.dept_id):
            raise errors.NotFoundError(msg='Department does not exist')
        for role_id in obj.roles:
            if not await role_dao.get(db, role_id):
                raise errors.NotFoundError(msg='Role does not exist')
        await user_dao.add(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateUserParam) -> int:
        """
        Update user information

        :param db: Database session
        :param pk: User ID
        :param obj: User update parameters
        :return:
        """
        user = await user_dao.get_with_relation(db, user_id=pk)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        if obj.username != user.username and await user_dao.get_by_username(db, obj.username):
            raise errors.ConflictError(msg='Username already registered')
        for role_id in obj.roles:
            if not await role_dao.get(db, role_id):
                raise errors.NotFoundError(msg='Role does not exist')
        count = await user_dao.update(db, user, obj)
        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def update_permission(*, db: AsyncSession, request: Request, pk: int, type: UserPermissionType) -> int:  # noqa: C901
        """
        Update user permission

        :param db: Database session
        :param request: FastAPI request object
        :param pk: User ID
        :param type: Permission type
        :return:
        """
        match type:
            case UserPermissionType.superuser:
                user = await user_dao.get(db, pk)
                if not user:
                    raise errors.NotFoundError(msg='User does not exist')
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Cannot modify own permissions')
                count = await user_dao.set_super(db, pk, is_super=not user.status)
            case UserPermissionType.staff:
                user = await user_dao.get(db, pk)
                if not user:
                    raise errors.NotFoundError(msg='User does not exist')
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Cannot modify own permissions')
                count = await user_dao.set_staff(db, pk, is_staff=not user.is_staff)
            case UserPermissionType.status:
                user = await user_dao.get(db, pk)
                if not user:
                    raise errors.NotFoundError(msg='User does not exist')
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Cannot modify own permissions')
                count = await user_dao.set_status(db, pk, 0 if user.status == 1 else 1)
            case UserPermissionType.multi_login:
                user = await user_dao.get(db, pk)
                if not user:
                    raise errors.NotFoundError(msg='User does not exist')
                multi_login = user.is_multi_login if pk != user.id else request.user.is_multi_login
                new_multi_login = not multi_login
                count = await user_dao.set_multi_login(db, pk, multi_login=new_multi_login)
                token = get_token(request)
                token_payload = jwt_decode(token)
                if pk == user.id:
                    # When system admin modifies self, invalidate all tokens except current
                    if not new_multi_login:
                        key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                        await redis_client.delete_prefix(
                            key_prefix,
                            exclude=f'{key_prefix}:{token_payload.session_uuid}',
                        )
                else:
                    # When system admin modifies others, invalidate all their tokens
                    if not new_multi_login:
                        key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                        await redis_client.delete_prefix(key_prefix)
            case _:
                raise errors.RequestError(msg='Permission type does not exist')

        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def reset_password(*, db: AsyncSession, pk: int, password: str) -> int:
        """
        Reset user password

        :param db: Database session
        :param pk: User ID
        :param password: New password
        :return:
        """
        user = await user_dao.get(db, pk)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        count = await user_dao.reset_password(db, user.id, password)
        key_prefix = [
            f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
            f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}',
        ]
        for prefix in key_prefix:
            await redis_client.delete(prefix)
        return count

    @staticmethod
    async def update_nickname(*, db: AsyncSession, request: Request, nickname: str) -> int:
        """
        Update current user nickname

        :param db: Database session
        :param request: FastAPI request object
        :param nickname: User nickname
        :return:
        """
        token = get_token(request)
        token_payload = jwt_decode(token)
        user = await user_dao.get(db, token_payload.id)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        count = await user_dao.update_nickname(db, token_payload.id, nickname)
        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def update_avatar(*, db: AsyncSession, request: Request, avatar: str) -> int:
        """
        Update current user avatar

        :param db: Database session
        :param request: FastAPI request object
        :param avatar: Avatar URL
        :return:
        """
        token = get_token(request)
        token_payload = jwt_decode(token)
        user = await user_dao.get(db, token_payload.id)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        count = await user_dao.update_avatar(db, token_payload.id, avatar)
        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def update_email(*, db: AsyncSession, request: Request, captcha: str, email: str) -> int:
        """
        Update current user email

        :param db: Database session
        :param request: FastAPI request object
        :param captcha: Email verification code
        :param email: Email
        :return:
        """
        token = get_token(request)
        token_payload = jwt_decode(token)
        user = await user_dao.get(db, token_payload.id)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        captcha_code = await redis_client.get(f'{settings.EMAIL_CAPTCHA_REDIS_PREFIX}:{ctx.ip}')
        if not captcha_code:
            raise errors.RequestError(msg='Verification code has expired, please retrieve again')
        if captcha != captcha_code:
            raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
        await redis_client.delete(f'{settings.EMAIL_CAPTCHA_REDIS_PREFIX}:{ctx.ip}')
        count = await user_dao.update_email(db, token_payload.id, email)
        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def update_password(*, db: AsyncSession, request: Request, obj: ResetPasswordParam) -> int:
        """
        Update current user password

        :param db: Database session
        :param request: FastAPI request object
        :param obj: Password reset parameters
        :return:
        """
        token = get_token(request)
        token_payload = jwt_decode(token)
        user = await user_dao.get(db, token_payload.id)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        if not password_verify(obj.old_password, user.password):
            raise errors.RequestError(msg='Old password is incorrect')
        if obj.new_password != obj.confirm_password:
            raise errors.RequestError(msg='Passwords do not match')
        count = await user_dao.reset_password(db, user.id, obj.new_password)
        key_prefix = [
            f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
            f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}',
        ]
        for prefix in key_prefix:
            await redis_client.delete_prefix(prefix)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        Delete user

        :param db: Database session
        :param pk: User ID
        :return:
        """
        user = await user_dao.get(db, pk)
        if not user:
            raise errors.NotFoundError(msg='User does not exist')
        count = await user_dao.delete(db, user.id)
        key_prefix = [
            f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
        ]
        for key in key_prefix:
            await redis_client.delete_prefix(key)
        return count


user_service: UserService = UserService()
