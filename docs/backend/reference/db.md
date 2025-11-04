---
title: Switching Database
---

::: caution
Since v1.10.0, fba has replaced MySQL with PostgreSQL as the default database
:::

fba supports PostgreSQL and MySQL. The default configuration uses PostgreSQL.

## Docker Images

If you haven't installed locally or prefer using Docker images:

### PostgreSQL

```shell:no-line-numbers
docker run -d \
  --name fba_postgres \
  --restart always \
  -e POSTGRES_DB='fba' \
  -e POSTGRES_PASSWORD='123456' \
  -e TZ='Asia/Shanghai' \
  -v fba_postgres:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

### MySQL

```shell:no-line-numbers
docker run -d \
  --name fba_mysql \
  --restart always \
  -e MYSQL_DATABASE=fba \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e TZ=Asia/Shanghai \
  -v fba_mysql:/var/lib/mysql \
  -p 3306 \
  mysql:8.0.41 \
  --default-authentication-plugin=mysql_native_password \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_general_ci \
  --lower_case_table_names=1
```

## Environment Configuration

PostgreSQL and MySQL differ in username, port, etc. If you created Docker images using the above commands, modify `.env`
with the following partial configuration. Otherwise, adjust according to your actual setup.

### PostgreSQL

```dotenv:no-line-numbers
# Database
DATABASE_TYPE='postgresql'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=5432
DATABASE_USER='postgres'
DATABASE_PASSWORD='123456'
```

### MySQL

```dotenv:no-line-numbers
# Database
DATABASE_TYPE='mysql'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=3306
DATABASE_USER='root'
DATABASE_PASSWORD='123456'
```

## Decoupling

- Remove `with_variant` related code (if present), keeping only the corresponding database type
- Remove `DATABASE_TYPE` and its related calls from `backend/core/conf.py`
- Remove `DATABASE_TYPE` from `.env_example` and `.env`
- Update `database_type` related code in `backend/templates/py/model.jinja`
- Delete either the `postgresql` or `mysql` folder in the `backend/sql` directory
- Remove the `fba_postgres` or `fba_mysql` container script from `docker-compose.yml`
