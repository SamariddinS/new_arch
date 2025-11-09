from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    """Data rule base model"""

    name: str = Field(description='Rule name')
    model: str = Field(description='Model name')
    column: str = Field(description='Column name')
    operator: RoleDataRuleOperatorType = Field(description='Operator (AND/OR)')
    expression: RoleDataRuleExpressionType = Field(description='Expression type')
    value: str = Field(description='Rule value')


class CreateDataRuleParam(DataRuleSchemaBase):
    """Create data rule parameters"""


class UpdateDataRuleParam(DataRuleSchemaBase):
    """Update data rule parameters"""


class DeleteDataRuleParam(SchemaBase):
    """Delete data rule parameters"""

    pks: list[int] = Field(description='Rule ID list')


class GetDataRuleDetail(DataRuleSchemaBase):
    """Data rule detail"""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int = Field(description='Rule ID')
    created_time: datetime = Field(description='Creation time')
    updated_time: datetime | None = Field(None, description='Update time')


class GetDataRuleColumnDetail(SchemaBase):
    """Data rule available model column detail"""

    key: str = Field(description='Column name')
    comment: str = Field(description='Column comment')
