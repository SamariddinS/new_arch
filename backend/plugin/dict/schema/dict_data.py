from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictDataSchemaBase(SchemaBase):
    """Dictionary data base schema"""

    type_id: int = Field(description='Dictionary type ID')
    label: str = Field(description='Dictionary label')
    value: str = Field(description='Dictionary value')
    color: str | None = Field(None, description='Label color')
    sort: int = Field(description='Sort order')
    status: StatusType = Field(description='Status')
    remark: str | None = Field(None, description='Remark')


class CreateDictDataParam(DictDataSchemaBase):
    """Create dictionary data parameters"""


class UpdateDictDataParam(DictDataSchemaBase):
    """Update dictionary data parameters"""


class DeleteDictDataParam(SchemaBase):
    """Delete dictionary data parameters"""

    pks: list[int] = Field(description='Dictionary data ID list')


class GetDictDataDetail(DictDataSchemaBase):
    """Dictionary data details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Dictionary data ID')
    type_code: str = Field(description='Dictionary type code')
    created_time: datetime = Field(description='Created time')
    updated_time: datetime | None = Field(None, description='Updated time')
