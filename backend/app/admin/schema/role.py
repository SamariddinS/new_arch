from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_scope import GetDataScopeWithRelationDetail
from backend.app.admin.schema.menu import GetMenuDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    """Role base model"""

    name: str = Field(description='Role name')
    status: StatusType = Field(description='Status')
    is_filter_scopes: bool = Field(True, description='Filter data permissions')
    remark: str | None = Field(None, description='Remark')


class CreateRoleParam(RoleSchemaBase):
    """Create role parameters"""


class UpdateRoleParam(RoleSchemaBase):
    """Update role parameters"""


class DeleteRoleParam(SchemaBase):
    """Delete role parameters"""

    pks: list[int] = Field(description='Role ID list')


class UpdateRoleMenuParam(SchemaBase):
    """Update role menu parameters"""

    menus: list[int] = Field(description='Menu ID list')


class UpdateRoleScopeParam(SchemaBase):
    """Update role data scope parameters"""

    scopes: list[int] = Field(description='Data scope ID list')


class GetRoleDetail(RoleSchemaBase):
    """Role detail"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='Role ID')
    created_time: datetime = Field(description='Creation time')
    updated_time: datetime | None = Field(None, description='Update time')


class GetRoleWithRelationDetail(GetRoleDetail):
    """Role with relation detail"""

    menus: list[GetMenuDetail | None] = Field([], description='Menu detail list')
    scopes: list[GetDataScopeWithRelationDetail | None] = Field([], description='Data Range List')
