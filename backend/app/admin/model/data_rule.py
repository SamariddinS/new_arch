from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_data_scope_rule
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataScope


class DataRule(Base):
    """Data rule table"""

    __tablename__ = 'sys_data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(512), unique=True, comment='Name')
    model: Mapped[str] = mapped_column(sa.String(64), comment='SQLA model name, corresponding to DATA_PERMISSION_MODELS key')
    column: Mapped[str] = mapped_column(sa.String(32), comment='Model column name')
    operator: Mapped[int] = mapped_column(comment='Operator (0=and 1=or)')
    expression: Mapped[int] = mapped_column(
        comment='Expression (0== 1!= 2> 3>= 4< 5<= 6=in 7=not_in)',
    )
    value: Mapped[str] = mapped_column(sa.String(256), comment='Rule value')

    # Data scope rule many-to-many
    scopes: Mapped[list[DataScope]] = relationship(init=False, secondary=sys_data_scope_rule, back_populates='rules')
