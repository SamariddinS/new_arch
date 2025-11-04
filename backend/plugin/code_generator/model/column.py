from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import DataClassBase, UniversalText, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenBusiness


class GenColumn(DataClassBase):
    """Code generation model column table"""

    __tablename__ = 'gen_column'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), comment='Column name')
    comment: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='Column description')
    type: Mapped[str] = mapped_column(sa.String(32), default='String', comment='SQLA model column type')
    pd_type: Mapped[str] = mapped_column(sa.String(32), default='str', comment='Pydantic type corresponding to column type')
    default: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='Column default value')
    sort: Mapped[int | None] = mapped_column(default=1, comment='Column sort order')
    length: Mapped[int] = mapped_column(default=0, comment='Column length')
    is_pk: Mapped[bool] = mapped_column(default=False, comment='Is primary key')
    is_nullable: Mapped[bool] = mapped_column(default=False, comment='Is nullable')

    # Code generation business model columns one-to-many
    gen_business_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey('gen_business.id', ondelete='CASCADE'), default=0, comment='Code generation business ID'
    )
    gen_business: Mapped[GenBusiness | None] = relationship(init=False, back_populates='gen_column')
