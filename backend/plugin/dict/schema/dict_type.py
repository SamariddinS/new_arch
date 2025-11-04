from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DictTypeSchemaBase(SchemaBase):
    """Dictionary type base schema"""

    name: str = Field(description='Dictionary name')
    code: str = Field(description='Dictionary code')
    remark: str | None = Field(None, description='Remark')


class CreateDictTypeParam(DictTypeSchemaBase):
    """Create dictionary type parameters"""


class UpdateDictTypeParam(DictTypeSchemaBase):
    """Update dictionary type parameters"""


class DeleteDictTypeParam(SchemaBase):
    """Delete dictionary type parameters"""

    pks: list[int] = Field(description='Dictionary type ID list')


class GetDictTypeDetail(DictTypeSchemaBase):
    """Dictionary type details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Dictionary type ID')
    created_time: datetime = Field(description='Created time')
    updated_time: datetime | None = Field(None, description='Updated time')
