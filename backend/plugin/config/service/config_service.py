from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.config.crud.crud_config import config_dao
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    UpdateConfigParam,
    UpdateConfigsParam,
)


class ConfigService:
    """Configuration service class"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Config:
        """
        Get configuration details

        :param db: Database session
        :param pk: Configuration ID
        :return:
        """

        config = await config_dao.get(db, pk)
        if not config:
            raise errors.NotFoundError(msg='Configuration does not exist')
        return config

    @staticmethod
    async def get_all(*, db: AsyncSession, type: str | None) -> Sequence[Config | None]:
        """
        Get all configurations

        :param db: Database session
        :param type: Configuration type
        :return:
        """

        return await config_dao.get_all(db, type)

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, type: str | None) -> dict[str, Any]:
        """
        Get configuration list

        :param db: Database session
        :param name: Configuration name
        :param type: Configuration type
        :return:
        """
        config_select = await config_dao.get_select(name=name, type=type)
        return await paging_data(db, config_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        Create configuration

        :param db: Database session
        :param obj: Configuration create parameters
        :return:
        """

        config = await config_dao.get_by_key(db, obj.key)
        if config:
            raise errors.ConflictError(msg=f'Configuration {obj.key} already exists')
        await config_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update configuration

        :param db: Database session
        :param pk: Configuration ID
        :param obj: Configuration update parameters
        :return:
        """

        config = await config_dao.get(db, pk)
        if not config:
            raise errors.NotFoundError(msg='Configuration does not exist')
        if config.key != obj.key:
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ConflictError(msg=f'Configuration {obj.key} already exists')
        count = await config_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def bulk_update(*, db: AsyncSession, objs: list[UpdateConfigsParam]) -> int:
        """
        Bulk update configurations

        :param db: Database session
        :param objs: Configuration bulk update parameters
        :return:
        """

        for _batch in range(0, len(objs), 1000):
            for obj in objs:
                config = await config_dao.get(db, obj.id)
                if not config:
                    raise errors.NotFoundError(msg='Configuration does not exist')
                if config.key != obj.key:
                    config = await config_dao.get_by_key(db, obj.key)
                    if config:
                        raise errors.ConflictError(msg=f'Configuration {obj.key} already exists')
        count = await config_dao.bulk_update(db, objs)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pks: list[int]) -> int:
        """
        Bulk delete configurations

        :param db: Database session
        :param pks: Configuration ID list
        :return:
        """

        count = await config_dao.delete(db, pks)
        return count


config_service: ConfigService = ConfigService()
