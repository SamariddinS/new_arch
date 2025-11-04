from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import User


class Dept(Base):
    """Department table"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), comment='Department name')
    sort: Mapped[int] = mapped_column(default=0, comment='Sort order')
    leader: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='Leader')
    phone: Mapped[str | None] = mapped_column(sa.String(11), default=None, comment='Phone')
    email: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='Email')
    status: Mapped[int] = mapped_column(default=1, comment='Department status (0=disabled 1=normal)')
    del_flag: Mapped[bool] = mapped_column(default=False, comment='Delete flag (0=deleted 1=exists)')

    # Parent department one-to-many
    parent_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, sa.ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, index=True, comment='Parent department ID'
    )
    parent: Mapped[Dept | None] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list[Dept] | None] = relationship(init=False, back_populates='parent')

    # Department user one-to-many
    users: Mapped[list[User]] = relationship(init=False, back_populates='dept')
