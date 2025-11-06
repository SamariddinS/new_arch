from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LevelSchemaBase(SchemaBase):
    """Skill/experience level reference base model"""
    name: str = Field(description='Level name')
    status: bool = Field(description='Active status')


class CreateLevelParam(LevelSchemaBase):
    """Create Skill/experience level reference parameters"""


class UpdateLevelParam(LevelSchemaBase):
    """Update Skill/experience level reference parameters"""


class DeleteLevelParam(SchemaBase):
    """Delete Skill/experience level reference parameters"""

    pks: list[int] = Field(description='Skill/experience level reference ID list')


class GetLevelDetail(LevelSchemaBase):
    """Skill/experience level reference details"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
