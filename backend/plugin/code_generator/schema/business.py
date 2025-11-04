from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    """Code generation business base schema"""

    app_name: str = Field(description='Application name (English)')
    table_name: str = Field(description='Table name (English)')
    doc_comment: str = Field(description='Documentation comment (for function/parameter docs)')
    table_comment: str | None = Field(None, description='Table description')
    class_name: str | None = Field(None, description='Base class name for Python code')
    schema_name: str | None = Field(None, description='Base class name for Python Schema code')
    filename: str | None = Field(None, description='Base filename for Python code')
    default_datetime_column: bool = Field(True, description='Whether default datetime columns exist')
    api_version: str = Field('v1', description='Code generation API version')
    gen_path: str | None = Field(None, description='Code generation path')
    remark: str | None = Field(None, description='Remark')


class CreateGenBusinessParam(GenBusinessSchemaBase):
    """Create code generation business parameters"""


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    """Update code generation business parameters"""


class GetGenBusinessDetail(GenBusinessSchemaBase):
    """Get code generation business details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Primary key ID')
    created_time: datetime = Field(description='Created time')
    updated_time: datetime | None = Field(None, description='Updated time')
