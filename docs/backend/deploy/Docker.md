---
title: Docker Deployment
---

::: info
A solid tutorial site: Docker — From Beginner to Practice
:::

## Local Deployment

Local deployment quickly provides a local API service.

### Backend

:::: steps

1. env

   In the `backend` directory, create the env file:

   ```shell:no-line-numbers
   touch .env
   ```

   Copy initial env values into the file:

   ```shell:no-line-numbers
   cp .env.example .env
   ```

2. Edit `backend/core/conf.py` and `.env` as needed
3. Build images

   From the project root, run:

   ::: warning
   If starting containers locally, change `127.0.0.1` to `host.docker.internal` in `.env`.
   :::

   ::: tabs#dockerfile
   @tab fba

   ```shell:no-line-numbers
   docker build -f Dockerfile -t fba_backend_independent .
   ```

   @tab celery

   ```shell:no-line-numbers
   docker build --build-arg SERVER_TYPE=celery -t fba_celery_independent .
   ```

   :::

4. Run containers

   Images don’t include databases. Ensure local PostgreSQL/MySQL and Redis are running.

   ::: tabs#dockerfile
   @tab fba

   ```shell:no-line-numbers
   docker run -d -p 8000:8000 --name fba_server fba_backend_independent
   ```

   @tab celery

   ```shell:no-line-numbers
   docker run -d -p 8555:8555 --name fba_celery fba_celery_independent
   ```

   :::

::::

### Frontend

See Frontend Quick Start: ../../frontend/summary/quick-start.md

## Server Deployment

::: warning
This guide uses HTTPS as an example.
:::

::: info
For free SSL, httpsok offers easy auto-renewal with one command; supports nginx, wildcard certs, Qiniu, Tencent Cloud, Alibaba Cloud, CDN, OSS, load balancers.
:::

### Backend

:::: steps

1. Pull code to the server

   Use SSH (safer) or HTTPS as you prefer.

2. env

   In `backend`, create the env file:

   ```shell:no-line-numbers
   touch .env
   ```

   Go to `deploy/backend/docker-compose` and edit `.env.server` as needed.

   ::: info
   The compose setup mounts `.env.server` into the container as fba’s env file. Editing it locally updates the container without rebuilding.
   :::

   ::: warning
   If using MySQL, adjust `.env.server`:

   ```dotenv:no-line-numbers
   # Database
   DATABASE_TYPE='mysql'
   DATABASE_HOST='fba_mysql'
   DATABASE_PORT=3306
   DATABASE_USER='root'
   DATABASE_PASSWORD='123456'
   ```

   :::

3. Edit `backend/core/conf.py` as needed

4. Update docker-compose as needed

   See comments in `docker-compose.yml` for guidance.

5. Start with one command

   From the project root, run:

   ::: warning
   If image pulls fail, troubleshoot per your environment.
   :::

   ```shell:no-line-numbers
   docker-compose up -d --build
   ```

6. Wait for completion
   ::::

### Frontend

See Frontend Docker deploy: ../../frontend/deploy/docker.md

## Notes

::: warning
Avoid frequent `docker-compose up -d --build`; it rebuilds and retains old containers, quickly consuming disk space.
:::

[15 Scripts for Automated Management of Docker Containers](https://www.yuque.com/fcant/devops/itkfyytisf9z84y6){.read-more}

Prune unused images

```shell:no-line-numbers
docker image prune
```

Prune unused containers

```shell:no-line-numbers
docker container prune
```

Prune all unused images, containers, networks, and build cache

```shell:no-line-numbers
docker system prune
```
