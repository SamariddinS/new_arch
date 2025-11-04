from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_menu
from backend.common.model import Base, UniversalText, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import Role


class Menu(Base):
    """Menu table"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(sa.String(64), comment='Menu title')
    name: Mapped[str] = mapped_column(sa.String(64), comment='Menu name')
    path: Mapped[str | None] = mapped_column(sa.String(200), comment='Route path')
    sort: Mapped[int] = mapped_column(default=0, comment='Sort order')
    icon: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='Menu icon')
    type: Mapped[int] = mapped_column(default=0, comment='Menu type (0=directory 1=menu 2=button 3=embedded 4=external)')
    component: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='Component path')
    perms: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='Permission identifier')
    status: Mapped[int] = mapped_column(default=1, comment='Menu status (0=disabled 1=normal)')
    display: Mapped[int] = mapped_column(default=1, comment='Whether to display (0=no 1=yes)')
    cache: Mapped[int] = mapped_column(default=1, comment='Whether to cache (0=no 1=yes)')
    link: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='External link address')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='Remark')

    # Parent menu one-to-many
    parent_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, sa.ForeignKey('sys_menu.id', ondelete='SET NULL'), default=None, index=True, comment='Parent menu ID'
    )
    parent: Mapped[Menu | None] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list[Menu] | None] = relationship(init=False, back_populates='parent')

    # Menu role many-to-many
    roles: Mapped[list[Role]] = relationship(init=False, secondary=sys_role_menu, back_populates='menus')
