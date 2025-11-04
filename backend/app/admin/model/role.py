from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_data_scope, sys_role_menu, sys_user_role
from backend.common.model import Base, UniversalText, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataScope, Menu, User


class Role(Base):
    """Role table"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), unique=True, comment='Role name')
    status: Mapped[int] = mapped_column(default=1, comment='Role status (0=disabled 1=normal)')
    is_filter_scopes: Mapped[bool] = mapped_column(default=True, comment='Filter data permissions (0=no 1=yes)')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='Remark')

    # Role user many-to-many
    users: Mapped[list[User]] = relationship(init=False, secondary=sys_user_role, back_populates='roles')

    # Role menu many-to-many
    menus: Mapped[list[Menu]] = relationship(init=False, secondary=sys_role_menu, back_populates='roles')

    # Role data scope many-to-many
    scopes: Mapped[list[DataScope]] = relationship(init=False, secondary=sys_role_data_scope, back_populates='roles')
