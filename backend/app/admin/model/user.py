from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_user_role
from backend.common.model import Base, TimeZone, id_key
from backend.database.db import uuid4_str
from backend.utils.timezone import timezone

if TYPE_CHECKING:
    from backend.app.admin.model import Dept, Role


class User(Base):
    """User table"""

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(sa.String(64), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(sa.String(64), unique=True, index=True, comment='Username')
    nickname: Mapped[str] = mapped_column(sa.String(64), comment='Nickname')
    password: Mapped[str | None] = mapped_column(sa.String(256), comment='Password')
    salt: Mapped[bytes | None] = mapped_column(sa.LargeBinary(255), comment='Encryption salt')
    email: Mapped[str | None] = mapped_column(sa.String(256), default=None, unique=True, index=True, comment='Email')
    phone: Mapped[str | None] = mapped_column(sa.String(11), default=None, comment='Phone number')
    avatar: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='Avatar')
    status: Mapped[int] = mapped_column(default=1, index=True, comment='User account status (0=disabled 1=normal)')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='Super permission (0=no 1=yes)')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='Backend admin login (0=no 1=yes)')
    is_multi_login: Mapped[bool] = mapped_column(default=False, comment='Allow multi login (0=no 1=yes)')
    join_time: Mapped[datetime] = mapped_column(TimeZone, init=False, default_factory=timezone.now, comment='Registration time')
    last_login_time: Mapped[datetime | None] = mapped_column(
        TimeZone, init=False, onupdate=timezone.now, comment='Last login'
    )

    # Department user one-to-many
    dept_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, sa.ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, comment='Department relation ID'
    )
    dept: Mapped[Dept | None] = relationship(init=False, back_populates='users')

    # User role many-to-many
    roles: Mapped[list[Role]] = relationship(init=False, secondary=sys_user_role, back_populates='users')
