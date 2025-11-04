from datetime import datetime
from typing import Annotated, Any

from pydantic import ConfigDict, Field, HttpUrl, PlainSerializer, model_validator
from typing_extensions import Self

from backend.app.admin.schema.dept import GetDeptDetail
from backend.app.admin.schema.role import GetRoleWithRelationDetail
from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase, ser_string


class AuthSchemaBase(SchemaBase):
    """User authentication base model"""

    username: str = Field(description='Username')
    password: str = Field(description='Password')


class AuthLoginParam(AuthSchemaBase):
    """User login parameters"""

    uuid: str = Field(description='Captcha UUID')
    captcha: str = Field(description='Captcha code')


class AddUserParam(AuthSchemaBase):
    """Add user parameters"""

    nickname: str | None = Field(None, description='Nickname')
    email: CustomEmailStr | None = Field(None, description='Email address')
    phone: CustomPhoneNumber | None = Field(None, description='Phone number')
    dept_id: int = Field(description='Department ID')
    roles: list[int] = Field(description='Role ID list')


class AddOAuth2UserParam(AuthSchemaBase):
    """Add OAuth2 user parameters"""

    password: str | None = Field(None, description='Password')
    nickname: str | None = Field(None, description='Nickname')
    email: CustomEmailStr | None = Field(None, description='Email address')
    avatar: Annotated[HttpUrl, PlainSerializer(ser_string)] | None = Field(None, description='Avatar URL')


class ResetPasswordParam(SchemaBase):
    """Reset password parameters"""

    old_password: str = Field(description='Old password')
    new_password: str = Field(description='New password')
    confirm_password: str = Field(description='Confirm password')


class UserInfoSchemaBase(SchemaBase):
    """User information base model"""

    dept_id: int | None = Field(None, description='Department ID')
    username: str = Field(description='Username')
    nickname: str = Field(description='Nickname')
    avatar: Annotated[HttpUrl, PlainSerializer(ser_string)] | None = Field(None, description='Avatar URL')
    email: CustomEmailStr | None = Field(None, description='Email address')
    phone: CustomPhoneNumber | None = Field(None, description='Phone number')


class UpdateUserParam(UserInfoSchemaBase):
    """Update user parameters"""

    roles: list[int] = Field(description='Role ID list')


class GetUserInfoDetail(UserInfoSchemaBase):
    """User information detail"""

    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = Field(None, description='Department ID')
    id: int = Field(description='User ID')
    uuid: str = Field(description='User UUID')
    status: StatusType = Field(description='Status')
    is_superuser: bool = Field(description='Is superuser')
    is_staff: bool = Field(description='Is staff')
    is_multi_login: bool = Field(description='Allow multi-device login')
    join_time: datetime = Field(description='Join time')
    last_login_time: datetime | None = Field(None, description='Last login time')


class GetUserInfoWithRelationDetail(GetUserInfoDetail):
    """User information with relation detail"""

    model_config = ConfigDict(from_attributes=True)

    dept: GetDeptDetail | None = Field(None, description='Department information')
    roles: list[GetRoleWithRelationDetail] = Field(description='Role list')


class GetCurrentUserInfoWithRelationDetail(GetUserInfoWithRelationDetail):
    """Current user information with relation detail"""

    model_config = ConfigDict(from_attributes=True)

    dept: str | None = Field(None, description='Department name')
    roles: list[str] = Field(description='Role name list')

    @model_validator(mode='before')
    @classmethod
    def handel(cls, data: Any) -> Self:
        """Process department and role data"""
        dept = data['dept']
        if dept:
            data['dept'] = dept['name']
        roles = data['roles']
        if roles:
            data['roles'] = [role['name'] for role in roles]
        return data
