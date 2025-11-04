from pydantic import Field

from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    """User social base schema"""

    sid: str = Field(description='Third-party user ID')
    source: UserSocialType = Field(description='Social platform')


class CreateUserSocialParam(UserSocialSchemaBase):
    """Create user social parameters"""

    user_id: int = Field(description='User ID')


class UpdateUserSocialParam(SchemaBase):
    """Update user social parameters"""
