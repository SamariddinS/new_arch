---
title: Operator
---

In common backend management systems, we often have information like creator and updater. How is this implemented? Let's discuss how to integrate operator information in fba.

In fba, operator information is not integrated into various database tables by default. However, we provide a very simple integration method: Mixin classes.

## How to integrate?

Open the backend directory of the fba project, enter the `common/model.py` file, and you'll see the `UserMixin` class standing there coldly, because fba
doesn't use it but only retains it.

```python
class UserMixin(MappedAsDataclass):
    """User Mixin dataclass"""

    created_by: Mapped[int] = mapped_column(sort_order=998, comment='Creator')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Updater')
```

## How to use?

First, the `UserMixin` class only stores the user's id, which is a common practice. So the question arises: How do I get the user id and store it?
When displaying in the backend, I certainly can't display the id, right? Let me answer these one by one.

### How to get user id and store it

The brilliance of our fba is that we fully utilize the request context feature. We store user information in each request's context through JWT middleware. Later, we will elaborate on the
JWT middleware. Then, we can easily read user information through the request object. In web frameworks like Django and Flask, request is a permanent guest.

First, in the API function, we should write request as the first parameter like Django/Flask, and it's best to add the parameter type: `request: Request`.
Then we can easily get the current operator id through `request.user.id` in the API function. Thus, when storing, this id can be added to the
schema or dictionary as stored data.

### I certainly can't display the id when displaying in the backend

Of course not. So what should we do? Although we only store the user id to the database, when we query single records or list queries, we need to intercept the data and replace the id with
username.

This involves another issue: where does the username come from? Considering performance impact, if we traverse these ids every time to query the database for replacement, it undoubtedly adds a lot of IO
operations. Therefore, we can set checkpoints (after new user registration, when querying user lists...) to cache all user ids and usernames to redis, and read from cache when replacing.

## Wouldn't it be better to directly store as username?

Of course you can. You can directly modify `UserMixin` to store as a string, then directly store the username through `request.user.username`. This way queries directly return usernames, eliminating the need for replacement operations.

## What exactly to store?

Whether to use id or username depends on the business scenario. If you need to always display the latest user information and avoid updating all historical data after users update their username, use
id. If username is unique and you need to preserve historical traces, directly use username.
