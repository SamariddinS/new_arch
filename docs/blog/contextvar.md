---
title: ContextVar: a powerful context manager for async programming
createTime: 2025-10-13 18:30
tags:
  - Python
---

In async and concurrent programming, how do we elegantly manage context-related state? Plain globals cause state pollution, and thread-local storage (`threading.local`) doesn’t fit nested async execution.

`ContextVar` solves this: within the same thread, each execution context (coroutine/task) can hold its own value without explicitly passing parameters.

## What is ContextVar?

`ContextVar` is the core class in `contextvars` for declaring and managing context variables. It’s like thread-local storage but designed for async execution. In `asyncio`, many coroutines can run on the same thread; globals easily “leak” state across tasks. `ContextVar` maintains a per-thread context stack so each `Context` holds snapshots, pushing on enter and rolling back on exit.

In short, `ContextVar` lets you implicitly access context-specific values (e.g., request trace ID) without parameter plumbing. This is common in web frameworks like FastAPI/Starlette.

## Core classes and methods

`contextvars` mainly offers `ContextVar`, `Token`, and `Context`:

### ContextVar

Declare a context variable.

- Constructor: `ContextVar(name, default=None)` where `name` is a debug label and `default` is the default value
- Methods:
  - `get(default=None)`: get the value or return `default`/raise `LookupError`
  - `set(value)`: set the value, returns a `Token` for rollback
  - `reset(token)`: restore the previous value using `Token`

### Token

Returned by `set()`, used to track and restore the previous value.

Has attributes like `old_value` and `var`. Since Python 3.14, `Token` supports context manager protocol for `with` blocks.

### Context

Represents a context mapping (like a dict) that manages variable state.

- `copy_context()`: copy the current context (O(1))
- `run(callable, *args, **kwargs)`: run a callable in the given context and rollback changes after

## Basic example

Suppose we have a `user_id` variable tracking the current user ID.

```python
import contextvars

# Declare the variable with default
user_id = contextvars.ContextVar('user_id', default='anonymous')

# Get current value
print(user_id.get())  # Output: anonymous

# Set a new value, returns Token
token = user_id.set('alice')
print(user_id.get())  # Output: alice

# Roll back using Token
user_id.reset(token)
print(user_id.get())  # Output: anonymous
```

Another example using `Token` as a context manager (Python 3.14+):

```python
user_id = contextvars.ContextVar('user_id', default='anonymous')

with user_id.set('bob'):
    print(user_id.get())  # Output: bob
    # inside the with block, reads see 'bob'

print(user_id.get())  # Output: anonymous (auto rollback)
```

This is safer than manual `reset`, avoiding forgotten rollbacks.

## In async programming

`ContextVar` shines in async scenarios. With `asyncio`, build a simple echo flow where each task stores an ID in context that other functions can read without parameters.

```python
import asyncio
import contextvars

# Declare task ID var
task_id_var = contextvars.ContextVar('task_id', default='none')

async def sub_task():
    # no param passing, read from context
    task_id = task_id_var.get()
    print(f"Sub task running with task_id: {task_id}")
    await asyncio.sleep(0.1)  # simulate work

async def main_task(task_id):
    token = task_id_var.set(task_id)
    try:
        await sub_task()
    finally:
        task_id_var.reset(token)

async def main():
    # run tasks concurrently
    await asyncio.gather(
        main_task('task1'),
        main_task('task2')
    )

# run
asyncio.run(main())
```

You will see output like:

```text
Sub task running with task_id: task1
Sub task running with task_id: task2
```

Here `sub_task()` doesn’t need the task ID parameter; it reads from the current context. Even with `asyncio.gather`, values are isolated per task. This removes parameter plumbing, especially in deep async call chains.

Another common case is logging: in ASGI apps, put the request ID in a `ContextVar` and inject it into logs downstream.

## ContextVar vs threading.local

`threading.local` provides per-thread storage for multithreaded programs. In async code, coroutines share a thread, so `local` values leak across tasks.

`ContextVar` is based on execution context stacks, supporting nested/cross coroutine switches. Each task/generator has its own view; changes roll back on exit.

If you’re on `asyncio`, prefer `ContextVar`.

## Notes

- Create at module top-level to avoid leaks via closures
- Use `default` to avoid `LookupError`; beware shared defaults in async
- Python 3.7+ support and native `asyncio` integration; threads have separate stacks
- For debugging, use `name` and `Context.items()`
