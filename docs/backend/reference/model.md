---
title: Model
---

Common models are located in the `backend/common/model.py` file

## Primary Key

We do not provide an automatic primary key mode; primary keys must be declared manually.

### Auto-increment ID

```python
# Generic Mapped type primary key, must be added manually, refer to the following usage
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
```

## Mixin Classes

[Mixin](https://en.wikipedia.org/wiki/Mixin) is an object-oriented programming concept that makes structure clearer

### Operator

Used to integrate operator information into database tables

[Please refer to **Operator**](operator.md){.read-more}

### DateTime

Used to integrate datetime into database tables, already integrated in the [Base](#base-base-class) base class

```python
class DateTimeMixin(MappedAsDataclass):
    """DateTime Mixin dataclass"""

    created_time: Mapped[datetime] = mapped_column(
        TimeZone, init=False, default_factory=timezone.now, sort_order=999, comment='Creation time'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        TimeZone, init=False, onupdate=timezone.now, sort_order=999, comment='Update time'
    )
```

## Dataclass Base Class

[MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses)

Declarative dataclass base class with dataclass integration, allowing for more advanced configuration, ==but without datetime integration=={.note}

```python
class DataClassBase(MappedAsDataclass, MappedBase):

    __abstract__ = True
```

## Base Base Class

Declarative dataclass base class with both dataclass and datetime integration

```python
class Base(DataClassBase, DateTimeMixin):

    __abstract__ = True
```
