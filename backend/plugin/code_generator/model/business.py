from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, UniversalText, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenColumn


class GenBusiness(Base):
    """Code generation business table"""

    __tablename__ = 'gen_business'

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(sa.String(64), comment='Application name (English)')
    table_name: Mapped[str] = mapped_column(sa.String(256), unique=True, comment='Table name (English)')
    doc_comment: Mapped[str] = mapped_column(sa.String(256), comment='Documentation comment (for function/parameter docs)')
    table_comment: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='Table description')
    # relate_model_fk: Mapped[int | None] = mapped_column(default=None, comment='Related table foreign key')
    class_name: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='Base class name (defaults to English table name)')
    schema_name: Mapped[str | None] = mapped_column(
        sa.String(64), default=None, comment='Schema name (defaults to English table name)'
    )
    filename: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='Base filename (defaults to English table name)')
    default_datetime_column: Mapped[bool] = mapped_column(default=True, comment='Whether default datetime columns exist')
    api_version: Mapped[str] = mapped_column(sa.String(32), default='v1', comment='Code generation API version, defaults to v1')
    gen_path: Mapped[str | None] = mapped_column(
        sa.String(256), default=None, comment='Code generation path (defaults to app root path)'
    )
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='Remark')
    # Code generation business model columns one-to-many
    gen_column: Mapped[list[GenColumn]] = relationship(init=False, back_populates='gen_business')
