from datetime import datetime
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, Text, TypeDecorator
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.core.conf import settings
from backend.utils.snowflake import snowflake
from backend.utils.timezone import timezone

# Common Mapped type primary key, needs to be added manually, refer to the following usage:
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int,
    mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
        sort_order=-999,
        comment='Primary key ID',
    ),
]


# Snowflake algorithm Mapped type primary key, same usage as id_key
# Details: https://fastapi-practices.github.io/fastapi_best_architecture_docs/backend/reference/pk.html
snowflake_id_key = Annotated[
    int,
    mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        index=True,
        default=snowflake.generate,
        sort_order=-999,
        comment='Snowflake algorithm primary key ID',
    ),
]


class UniversalText(TypeDecorator[str]):
    """PostgreSQL and MySQL compatible (long) text type"""

    impl = LONGTEXT if settings.DATABASE_TYPE == 'mysql' else Text
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect) -> str | None:  # noqa: ANN001
        return value

    def process_result_value(self, value: str | None, dialect) -> str | None:  # noqa: ANN001
        return value


class TimeZone(TypeDecorator[datetime]):
    """PostgreSQL and MySQL compatible timezone-aware type"""

    impl = DateTime(timezone=True)
    cache_ok = True

    @property
    def python_type(self) -> type[datetime]:
        return datetime

    def process_bind_param(self, value: datetime | None, dialect) -> datetime | None:  # noqa: ANN001
        if value is not None and value.utcoffset() != timezone.now().utcoffset():
            # TODO Handle daylight saving time offset
            value = timezone.from_datetime(value)
        return value

    def process_result_value(self, value: datetime | None, dialect) -> datetime | None:  # noqa: ANN001
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.tz_info)
        return value


# Mixin: An object-oriented programming concept that makes structure clearer, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """User Mixin dataclass"""

    created_by: Mapped[int] = mapped_column(sort_order=998, comment='Creator')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Updater')


class DateTimeMixin(MappedAsDataclass):
    """DateTime Mixin dataclass"""

    created_time: Mapped[datetime] = mapped_column(
        TimeZone,
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment='Created time',
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        TimeZone,
        init=False,
        onupdate=timezone.now,
        sort_order=999,
        comment='Updated time',
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    Declarative base class, exists as parent class of all base classes or data model classes

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        """Generate table name"""
        return self.__name__.lower()

    @declared_attr.directive
    def __table_args__(self) -> dict:
        """Table configuration"""
        return {'comment': self.__doc__ or ''}


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declarative dataclass base class, with dataclass integration, allows using more advanced configuration, but you must pay attention to some of its characteristics, especially when used with DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Declarative dataclass base class, with dataclass integration, and includes MiXin dataclass base table structure
    """

    __abstract__ = True
