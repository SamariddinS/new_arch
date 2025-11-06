import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Level(Base):
    """Skill/experience level reference"""

    __tablename__ = 'level'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(512), unique=True, sort_order=2, comment='Level name')
    status: Mapped[bool] = mapped_column(sa.BOOLEAN(), default=True, sort_order=3, comment='Active status')
