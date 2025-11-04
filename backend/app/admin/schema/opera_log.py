from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OperaLogSchemaBase(SchemaBase):
    """Operation log base model"""

    trace_id: str = Field(description='Trace ID')
    username: str | None = Field(None, description='Username')
    method: str = Field(description='Request method')
    title: str = Field(description='Operation title')
    path: str = Field(description='Request path')
    ip: str = Field(description='IP address')
    country: str | None = Field(None, description='Country')
    region: str | None = Field(None, description='Region')
    city: str | None = Field(None, description='City')
    user_agent: str = Field(description='User agent')
    os: str | None = Field(None, description='Operating system')
    browser: str | None = Field(None, description='Browser')
    device: str | None = Field(None, description='Device')
    args: dict[str, Any] | None = Field(None, description='Request arguments')
    status: StatusType = Field(description='Status')
    code: str = Field(description='Status code')
    msg: str | None = Field(None, description='Message')
    cost_time: float = Field(description='Cost time')
    opera_time: datetime = Field(description='Operation time')


class CreateOperaLogParam(OperaLogSchemaBase):
    """Create operation log parameters"""


class UpdateOperaLogParam(OperaLogSchemaBase):
    """Update operation log parameters"""


class DeleteOperaLogParam(SchemaBase):
    """Delete operation log parameters"""

    pks: list[int] = Field(description='Operation log ID list')


class GetOperaLogDetail(OperaLogSchemaBase):
    """Operation log detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Log ID')
    created_time: datetime = Field(description='Creation time')
