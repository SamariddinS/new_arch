from typing import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.reference.model import Level
from backend.app.reference.schema.level import CreateLevelParam, UpdateLevelParam


class CRUDLevel(CRUDPlus[Level]):
    async def get(self, db: AsyncSession, pk: int) -> Level | None:
        """
        Get Skill/experience level reference

        :param db: Database session
        :param pk: Skill/experience level reference ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_select(self) -> Select:
        """Get Skill/experience level reference list query expression"""
        return await self.select_order('id', 'desc')

    async def get_list_select(self) -> Select:
        """Get Skill/experience level reference simple list query expression"""
        return select(self.model).where(self.model.status == True).order_by(self.model.name.asc())

    async def get_all(self, db: AsyncSession) -> Sequence[Level]:
        """
        Get all Skill/experience level reference

        :param db: Database session
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateLevelParam) -> None:
        """
        Create Skill/experience level reference

        :param db: Database session
        :param obj: Create Skill/experience level reference parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateLevelParam) -> int:
        """
        Update Skill/experience level reference

        :param db: Database session
        :param pk: Skill/experience level reference ID
        :param obj: Update Skill/experience level reference parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Batch delete Skill/experience level reference

        :param db: Database session
        :param pks: Skill/experience level reference ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


level_dao: CRUDLevel = CRUDLevel(Level)
