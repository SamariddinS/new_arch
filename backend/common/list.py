from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

SchemaT = TypeVar('SchemaT')


class LabelValue(BaseModel):
    """Label-value pair for dropdown/select options"""

    label: str = Field(description='Display label')
    value: str = Field(description='Actual value')


class ListData(BaseModel, Generic[SchemaT]):
    """
    Unified return model for simple list responses

    E.g. ::

        @router.get('/test', response_model=ResponseSchemaModel[ListData[LabelValue]])
        def test():
            return ResponseSchemaModel[ListData[LabelValue]](data=ListData(items=[...]))

        @router.get('/test')
        def test() -> ResponseSchemaModel[ListData[LabelValue]]:
            return ResponseSchemaModel[ListData[LabelValue]](data=ListData(items=[...]))
    """

    items: Sequence[SchemaT] = Field(default_factory=list, description='List items')


async def get_list_data(db: AsyncSession, select: Select) -> Sequence[Any]:
    """
    Get simple list data based on SQLAlchemy select statement

    :param db: Database session
    :param select: SQL query statement
    :return: List of model instances
    """
    result = await db.execute(select)
    items = result.scalars().all()
    return items


def convert_to_label_value(
    items: Sequence[Any],
    label_field: str = 'name',
    value_field: str = 'id',
) -> list[LabelValue]:
    """
    Convert model instances to label-value pairs

    :param items: Sequence of model instances
    :param label_field: Field name to use as label
    :param value_field: Field name to use as value
    :return: List of LabelValue objects
    """
    return [
        LabelValue(
            label=str(getattr(item, label_field, '')),
            value=str(getattr(item, value_field, '')),
        )
        for item in items
    ]
