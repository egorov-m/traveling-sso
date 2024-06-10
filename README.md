<h1 align="center">
    <span>Traveling SSO</span>
</h1>

<div align="center">

Design and development of distributed software systems: semester work - auth, userInfo microservice.

[![Build][build-img]][build-url]
[![Tests][tests-img]][tests-url]

</div>


## Usage

### Deployed Staging Instance

`https://egorov-m-traveling-sso.hf.space/api/v1/docs`

### Configuration

**IS_REFRESH_TOKEN_VIA_COOKIE = `False`**

In an expanded instance, the refresh token is passed in the response body. Due to different domains, cookies will not be accessible.

*other default settings.*

### Local launch in docker

```shell
> docker compose up -d
```

**Swagger docs will be available:** http://localhost:33380/api/v1/docs

### Default init

- database is initialized via alembic migrations;
- root user admin is created, documents are added (Passport RF, Foreign Passport RF), client is created;


- service can be configured via environment variables, see [here](./src/traveling_sso/config.py);


- **User:**
  - id: `af5b620f-ecb5-40a6-ad5b-0a87a3bf9ff3`
  - email: `admin@example.com`
  - username: `admin`
  - role: `admin`
  - password: `123456789`
  - ...


- **Client:**
  - id: `77961ae0-25f3-4ec0-ac80-6e62d69f4f8c`
  - client_id: `Rh4ZomeoWHFJus8KbspWqJTtXHcMGkLHAZ30qgCD3RK3rTHJ`
  - client_public_secret: `-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1OC6GKv+z0FMIw+yx2B7\nKp8HE++UVc7oaOraWHy1DwuBrc29P9+fFBysxWbxvWY5npgTarC9hsPMJ3mV4QpS\nTTa6PVaxhUnzx5MsYcPCZ3DJ7DUk50Vdpoi12NywPZL5JU1d12VbDtGO1CiOJNLK\n1CPz0gxl5BnChSpDIuPa3k1B9okHH507KCiZVRPkA5bTuUbcq7u0CUkvQ3PY/VkJ\ncyEjgnr6WbtEmDT98hHrgMTbwNOpESKoK6A9y4+am/7jp+K/tSFZ7s6ExnP0BvD5\num8+qfTFRKQjLdOwjSWFMlo9NmiaelD7EUvT+LJCeXXI8cZe7Xg8EfWLzvUhaMMB\ndQIDAQAB\n-----END PUBLIC KEY-----`;
  - ...

**client_public_secret - \n line breaks* 

### How to register a user

1. Use the endpoint `POST /api/v1/auth/signup`;
2. Query parameter: client_id = `Rh4ZomeoWHFJus8KbspWqJTtXHcMGkLHAZ30qgCD3RK3rTHJ` - client initialized by default, assigned to admin user;
3. In request body: email = `<your_email>` - format is important, password = `<your_password>` - [8, 255] characters;

### How to signin a user

1. Use the endpoint `POST /api/v1/auth/signin`;
2. Query parameter: client_id = `Rh4ZomeoWHFJus8KbspWqJTtXHcMGkLHAZ30qgCD3RK3rTHJ` - client initialized by default, assigned to admin user;
3. In request body: login = `<your_email_or_username>`, password = `<your_password>`;
4. From the response body get an access token for authorized access. Use the following format in request headers: `Authorization: Bearer <your_access_token>`;
5. In addition to the access token, a refresh token (in the cookie or response body - depending on the configuration).
6. A session is created with each signin - default limit is 5. If the limit is exceeded, all old sessions will be revoked.

*ps. in default deployment, admin user data (login -`admin@example.com`, password - `123456789`) can be used for tests;*

### How to refresh a session (get a new access token)

1. Use the endpoint `POST /api/v1/auth/session/refresh`;
2. Pass in a cookie (sso_refresh_token) or as a header (x-sso-refresh-token) refresh token;
3. The response comes with a new access token and an updated refresh token.
4. The old access token is valid, until it expires. Old refresh token is not valid - new value is issued.

### How to logout a user

1. Use the endpoint `POST /api/v1/auth/logout`;
2. The current session will be revoked (determined by the passed access token). But, the access token will be valid until it expires - it should be removed on the frontend.

### How to revoke a user session

1. Use the endpoint `POST /api/v1/auth/session/revoke`;
2. Pass the session_id in the query parameter;
3. The refresh token for the specified session will be revoked. But, the access token will be valid until it expires - it should be removed on the frontend.

## Developing

- docker compose has configured volumes: `./src:/app/src`

```shell
> docker compose up -d
```

### Installing dependencies

- requires Python 3.11 + pip;

```shell
> python -m venv .venv
> source ./.venv/Scripts/activate  # Windows
> source ./.venv/bin/activate  # Linux
> pip install -r ./requirements/default.txt
> pip install -r ./requirements/tests.txt
```

### Testing

- requires instance Postgres database;
- setup environment;

```shell
export PYTHONPATH=./src \
export PYTHONUNBUFFERED=1 \
export SSO_HOST=localhost \
export SSO_PORT=33381 \
export DEBUG=False \
export INIT_ROOT_ADMIN_USER=False \
export DB_HOST=localhost \
export DB_PORT=<db_port> \
export POSTGRES_DB=<db_name> \
export POSTGRES_USER=<db_user> \
export POSTGRES_PASSWORD=<db_password>
```

```shell
pytest -v
```

#### Allure Report

```shell
pytest -v --alluredir docs/allure-results
allure generate docs/allure-results -o docs/allure-report --clean --single-file
allure serve docs/allure-results/
```

### Migration generation

```shell
> source ./.venv/Script/activate  # Windows
> source ./.venv/bin/activate  # Linux
> alembic -c src/traveling_sso/database/alembic.ini revision --autogenerate -m "<comment>"
> docker compose restart sso-service
```

[build-img]: https://github.com/egorov-m/traveling-sso/actions/workflows/docker-build.yaml/badge.svg?branch=develop
[build-url]: https://github.com/egorov-m/traveling-sso/actions
[tests-img]: https://github.com/egorov-m/traveling-sso/actions/workflows/tests.yaml/badge.svg?branch=develop
[tests-url]: https://egorov-m.github.io/traveling-sso/allure-report
