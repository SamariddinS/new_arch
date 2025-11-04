from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_data_scope_rule, sys_role_data_scope
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataRule, Role


class DataScope(Base):
    """Data scope table"""

    __tablename__ = 'sys_data_scope'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), unique=True, comment='Name')
    status: Mapped[int] = mapped_column(default=1, comment='Status (0=disabled 1=normal)')

    # Data scope rule many-to-many
    rules: Mapped[list[DataRule]] = relationship(init=False, secondary=sys_data_scope_rule, back_populates='scopes')

    # Role data scope many-to-many
    roles: Mapped[list[Role]] = relationship(init=False, secondary=sys_role_data_scope, back_populates='scopes')
