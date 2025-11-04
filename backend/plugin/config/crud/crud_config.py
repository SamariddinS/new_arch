from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import CreateConfigParam, UpdateConfigParam


class CRUDConfig(CRUDPlus[Config]):
    """System configuration database operations class"""

    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        Get configuration details

        :param db: Database session
        :param pk: Configuration ID
        :return:
        """
        return await self.select_model_by_column(db, id=pk)

    async def get_all(self, db: AsyncSession, type: str) -> Sequence[Config | None]:
        """
        Get configuration by key name

        :param db: Database session
        :param type: Configuration type
        :return:
        """
        return await self.select_models(db, type=type)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        Get configuration by key name

        :param db: Database session
        :param key: Configuration key name
        :return:
        """
        return await self.select_model_by_column(db, key=key)

    async def get_select(self, name: str | None, type: str | None) -> Select:
        """
        Get configuration list query expression

        :param name: Configuration name
        :param type: Configuration type
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if type is not None:
            filters['type__like'] = f'%{type}%'

        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        Create configuration

        :param db: Database session
        :param obj: Create configuration parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        Update configuration

        :param db: Database session
        :param pk: Configuration ID
        :param obj: Update configuration parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def bulk_update(self, db: AsyncSession, objs: list[UpdateConfigParam]) -> int:
        """
        Bulk update configurations

        :param db: Database session
        :param objs: Bulk update configuration parameters
        :return:
        """
        return await self.bulk_update_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Bulk delete configurations

        :param db: Database session
        :param pks: Configuration ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


config_dao: CRUDConfig = CRUDConfig(Config)
