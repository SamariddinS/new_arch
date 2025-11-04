---
title: OAuth 2.0
---

We integrate OAuth 2.0 in fba using [fastapi-oauth20](https://github.com/fastapi-practices/fastapi-oauth20). You can view our official implementation example in the `backend/plugin/oauth2` directory.

::: note
This authorization method is suitable for third-party platform authentication login. After successful third-party authorization, local users will be automatically created based on third-party platform information and automatically logged in. Users only need to approve third-party authorization.

However, to use this authorization method, you need to first understand OAuth 2.0 related knowledge and follow the third-party platform authentication requirements, obtain third-party platform authorization keys, and finally manually code the integration.
:::
