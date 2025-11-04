from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import User


class UserSocial(Base):
    """User social table (OAuth2)"""

    __tablename__ = 'sys_user_social'

    id: Mapped[id_key] = mapped_column(init=False)
    sid: Mapped[str] = mapped_column(sa.String(256), comment='Third-party user ID')
    source: Mapped[str] = mapped_column(sa.String(32), comment='Third-party user source')

    # User social info one-to-many
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey('sys_user.id', ondelete='CASCADE'), comment='User association ID'
    )
    user: Mapped[User | None] = relationship(init=False, backref='socials')
