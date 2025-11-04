from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.model import DataScope
from backend.app.admin.schema.data_scope import (
    CreateDataScopeParam,
    DeleteDataScopeParam,
    UpdateDataScopeParam,
    UpdateDataScopeRuleParam,
)
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.core.conf import settings
from backend.database.redis import redis_client


class DataScopeService:
    """Data scope service class"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> DataScope:
        """
        Get data scope details

        :param db: Database session
        :param pk: Scope ID
        :return:
        """

        data_scope = await data_scope_dao.get(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='Data scope does not exist')
        return data_scope

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[DataScope]:
        """
        Get all data scopes

        :param db: Database session
        :return:
        """

        data_scopes = await data_scope_dao.get_all(db)
        return data_scopes

    @staticmethod
    async def get_rules(*, db: AsyncSession, pk: int) -> DataScope:
        """
        Get data scope rules

        :param db: Database session
        :param pk: Scope ID
        :return:
        """

        data_scope = await data_scope_dao.get_with_relation(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='Data scope does not exist')
        return data_scope

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, status: int | None) -> dict[str, Any]:
        """
        Get data scope list

        :param db: Database session
        :param name: Scope name
        :param status: Scope status
        :return:
        """
        data_scope_select = await data_scope_dao.get_select(name, status)
        return await paging_data(db, data_scope_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDataScopeParam) -> None:
        """
        Create data scope

        :param db: Database session
        :param obj: Data scope parameters
        :return:
        """
        data_scope = await data_scope_dao.get_by_name(db, obj.name)
        if data_scope:
            raise errors.ConflictError(msg='Data scope already exists')
        await data_scope_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        Update data scope

        :param db: Database session
        :param pk: Scope ID
        :param obj: Data scope update parameters
        :return:
        """
        data_scope = await data_scope_dao.get(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='Data scope does not exist')
        if data_scope.name != obj.name and await data_scope_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg='Data scope already exists')
        count = await data_scope_dao.update(db, pk, obj)
        for role in await data_scope.awaitable_attrs.roles:
            for user in await role.awaitable_attrs.users:
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count

    @staticmethod
    async def update_data_scope_rule(*, db: AsyncSession, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        Update data scope rules

        :param pk: Scope ID
        :param rule_ids: Rule ID list
        :return:
        """
        count = await data_scope_dao.update_rules(db, pk, rule_ids)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteDataScopeParam) -> int:
        """
        Batch delete data scopes

        :param db: Database session
        :param obj: Scope ID list
        :return:
        """
        count = await data_scope_dao.delete(db, obj.pks)
        for pk in obj.pks:
            data_rule = await data_scope_dao.get(db, pk)
            if data_rule:
                for role in await data_rule.awaitable_attrs.roles:
                    for user in await role.awaitable_attrs.users:
                        await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count


data_scope_service: DataScopeService = DataScopeService()
