from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_rule import GetDataRuleDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DataScopeBase(SchemaBase):
    """Data scope base model"""

    name: str = Field(description='Name')
    status: StatusType = Field(description='Status')


class CreateDataScopeParam(DataScopeBase):
    """Create data scope parameters"""


class UpdateDataScopeParam(DataScopeBase):
    """Update data scope parameters"""


class UpdateDataScopeRuleParam(SchemaBase):
    """Update data scope rule parameters"""

    rules: list[int] = Field(description='Data rule ID list')


class DeleteDataScopeParam(SchemaBase):
    """Delete data scope parameters"""

    pks: list[int] = Field(description='Data scope ID list')


class GetDataScopeDetail(DataScopeBase):
    """Data scope detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Data scope ID')
    created_time: datetime = Field(description='Creation time')
    updated_time: datetime | None = Field(None, description='Update time')


class GetDataScopeWithRelationDetail(GetDataScopeDetail):
    """Data scope with relation detail"""

    rules: list[GetDataRuleDetail] = Field([], description='Data rule list')
