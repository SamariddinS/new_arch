from collections.abc import Sequence

from sqlalchemy import Select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, UpdateDictDataParam


class CRUDDictData(CRUDPlus[DictData]):
    """Dictionary data database operations"""

    async def get(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        Get dictionary data details

        :param db: Database session
        :param pk: Dictionary data ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies={'type': 'noload'})

    async def get_by_type_code(self, db: AsyncSession, type_code: str) -> Sequence[DictData]:
        """
        Get dictionary data by dictionary type code

        :param db: Database session
        :param type_code: Dictionary type code
        :return:
        """
        return await self.select_models_order(
            db,
            sort_columns='sort',
            sort_orders='desc',
            type_code=type_code,
            load_strategies={'type': 'noload'},
        )

    async def get_all(self, db: AsyncSession) -> Sequence[DictData]:
        """
        Get all dictionary data

        :param db: Database session
        :return:
        """
        return await self.select_models(db, load_strategies={'type': 'noload'})

    async def get_select(
        self,
        type_code: str | None,
        label: str | None,
        value: str | None,
        status: int | None,
        type_id: int | None,
    ) -> Select:
        """
        Get dictionary data list query expression

        :param type_code: Dictionary type code
        :param label: Dictionary data label
        :param value: Dictionary data value
        :param status: Dictionary status
        :param type_id: Dictionary type ID
        :return:
        """
        filters = {}

        if type_code is not None:
            filters['type_code'] = type_code
        if label is not None:
            filters['label__like'] = f'%{label}%'
        if value is not None:
            filters['value__like'] = f'%{value}%'
        if status is not None:
            filters['status'] = status
        if type_id is not None:
            filters['type_id'] = type_id

        return await self.select_order('id', 'desc', load_strategies={'type': 'noload'}, **filters)

    async def get_by_label_and_type_code(self, db: AsyncSession, label: str, type_code: str) -> DictData | None:
        """
        Get dictionary data by label and type code

        :param db: Database session
        :param label: Dictionary label
        :param type_code: Dictionary type code
        :return:
        """
        return await self.select_model_by_column(db, and_(self.model.label == label, self.model.type_code == type_code))

    async def create(self, db: AsyncSession, obj: CreateDictDataParam, type_code: str) -> None:
        """
        Create dictionary data

        :param db: Database session
        :param obj: Create dictionary data parameters
        :param type_code: Dictionary type code
        :return:
        """
        dict_obj = obj.model_dump()
        dict_obj.update({'type_code': type_code})
        new_data = self.model(**dict_obj)
        db.add(new_data)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictDataParam, type_code: str) -> int:
        """
        Update dictionary data

        :param db: Database session
        :param pk: Dictionary data ID
        :param obj: Update dictionary data parameters
        :param type_code: Dictionary type code
        :return:
        """
        dict_obj = obj.model_dump()
        dict_obj.update({'type_code': type_code})
        return await self.update_model(db, pk, dict_obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        Bulk delete dictionary data

        :param db: Database session
        :param pks: Dictionary data ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DictData | None:
        """
        Get dictionary data with related data

        :param db: Database session
        :param pk: Dictionary data ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies=['type'])


dict_data_dao: CRUDDictData = CRUDDictData(DictData)
