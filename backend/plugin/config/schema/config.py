from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ConfigSchemaBase(SchemaBase):
    """Parameter configuration base schema"""

    name: str = Field(description='Configuration name')
    type: str | None = Field(None, description='Configuration type')
    key: str = Field(description='Configuration key name')
    value: str = Field(description='Configuration value')
    is_frontend: bool = Field(description='Is frontend configuration')
    remark: str | None = Field(None, description='Remark')


class CreateConfigParam(ConfigSchemaBase):
    """Create configuration parameters"""


class UpdateConfigParam(ConfigSchemaBase):
    """Update configuration parameters"""


class UpdateConfigsParam(UpdateConfigParam):
    """Bulk update configuration parameters"""

    id: int = Field(description='Configuration ID')


class GetConfigDetail(ConfigSchemaBase):
    """Configuration details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Configuration ID')
    created_time: datetime = Field(description='Created time')
    updated_time: datetime | None = Field(None, description='Updated time')
