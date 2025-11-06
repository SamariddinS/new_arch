from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.reference.crud.crud_level import level_dao
from backend.app.reference.model import Level
from backend.app.reference.schema.level import CreateLevelParam, DeleteLevelParam, UpdateLevelParam
from backend.common.exception import errors
from backend.common.list import LabelValue, convert_to_label_value, get_list_data
from backend.common.pagination import paging_data


class LevelService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Level:
        """
        Get Skill/experience level reference

        :param db: Database session
        :param pk: Skill/experience level reference ID
        :return:
        """
        level = await level_dao.get(db, pk)
        if not level:
            raise errors.NotFoundError(msg='Skill/experience level reference not found')
        return level

    @staticmethod
    async def get_list(db: AsyncSession) -> dict[str, Any]:
        """
        Get Skill/experience level reference paginated list

        :param db: Database session
        :return:
        """
        level_select = await level_dao.get_select()
        return await paging_data(db, level_select)

    @staticmethod
    async def get_options(*, db: AsyncSession) -> list[LabelValue]:
        """
        Get Skill/experience level reference as label-value options list

        :param db: Database session
        :return:
        """
        level_select = await level_dao.get_list_select()
        items = await get_list_data(db, level_select)
        return convert_to_label_value(items, label_field='name', value_field='id')

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[Level]:
        """
        Get all Skill/experience level reference

        :param db: Database session
        :return:
        """
        levels = await level_dao.get_all(db)
        return levels

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateLevelParam) -> None:
        """
        Create Skill/experience level reference

        :param db: Database session
        :param obj: Create Skill/experience level reference parameters
        :return:
        """
        await level_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateLevelParam) -> int:
        """
        Update Skill/experience level reference

        :param db: Database session
        :param pk: Skill/experience level reference ID
        :param obj: Update Skill/experience level reference parameters
        :return:
        """
        count = await level_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteLevelParam) -> int:
        """
        Delete Skill/experience level reference

        :param db: Database session
        :param obj: Skill/experience level reference ID list
        :return:
        """
        count = await level_dao.delete(db, obj.pks)
        return count


level_service: LevelService = LevelService()
