---
title: APScheduler
---

In our initial framework implementation, we used APScheduler, but later we migrated to
Celery, for more details, please see: [#225](https://github.com/fastapi-practices/fastapi_best_architecture/discussions/225)

FastAPI + APScheduler is now released as a standalone repository. Its strengths lie in flexibility and real-time dynamic tasks. If you don't have heavy task requirements, it's a solid choice.

<LinkCard
title="fastapi_scheduler"
description="Scheduled Task Management Platform Built with FastAPI + APScheduler"
href="https://github.com/fastapi-practices/fastapi_scheduler"
icon="https://wu-clan.github.io/picx-images-hosting/logo/fba.png"
/>

::: warning
We plan to build APScheduler as an FBA solution.
Plugin, but requires waiting [4.0](https://github.com/agronholm/apscheduler/issues/465#issuecomment-2818889743)
Version Release
:::
