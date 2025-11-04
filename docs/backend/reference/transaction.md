---
title: Transactions
---

With engine `echo=True`, you’ll see transactions start even for queries. This isn’t misuse of SQLAlchemy. See discussions #6921 and #12782 for details.

::: Details Brief Summary
Any Python DBAPI/ORM compliant with PEP-249 starts transactions by default.

In SQLAlchemy you may avoid its transaction mode by configuring the database isolation level to `AUTOCOMMIT`. See docs on DBAPI-level autocommit.
:::

## CurrentSession

Mirrors the docs’ pattern; it doesn’t begin a transaction and is typically used for reads.

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Obtain database session"""
    async with async_db_session() as session:
        yield session

# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]
```

Usually applied directly to route handlers; considered thread-safe for session usage.

```python
@router.get('')
async def get_pagination_apis(db: CurrentSession) -> ResponseModel:
    ...
```

## CurrentSessionTransaction

Unlike `CurrentSession`, this automatically begins a transaction; use for create/update/delete.

```python
async def get_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """Obtain a database session with a transaction"""
    async with async_db_session.begin() as session:
        yield session

# Session Annotated
CurrentSessionTransaction = Annotated[AsyncSession, Depends(get_db_transaction)]
```

Usage is the same as `CurrentSession`.

```python
@router.post('')
async def get_pagination_apis(db: CurrentSession) -> ResponseModel:
    ...
```

## `begin()`

The SQLAlchemy-native way. Multiple calls in the same function may be less strict thread-safety-wise compared to the above annotations, but it can be used anywhere.

```python{2}
async def create(*, obj: CreateIns) -> None:
    async with async_db_session.begin() as db:
        await xxx_dao.create(db, obj)
```
