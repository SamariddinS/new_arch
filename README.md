# FastAPI Best Architecture

Enterprise-level backend architecture solution

## Pseudo 3-tier architecture

The mvc architecture is a common design pattern in python web, but the 3-tier architecture is even more fascinating

In python web development, there is no common standard for the concept of 3-tier architecture, so we'll call it a
pseudo 3-tier architecture here

But please note that we don't have a traditional multi-app structure (django, springBoot...) If you don't like this
pattern, use templates to transform it to your heart's content!

| workflow       | java           | fastapi_best_architecture |
|----------------|----------------|---------------------------|
| view           | controller     | api                       |
| data transmit  | dto            | schema                    |
| business logic | service + impl | service                   |
| data access    | dao / mapper   | crud                      |
| model          | model / entity | model                     |
