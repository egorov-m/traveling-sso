# traveling-sso
Design and development of distributed software systems: semester work - auth, userInfo microservice.


## Usage

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


## Developing

- docker compose has configured volumes: `./src:/app/src`

```shell
> docker compose up -d
> docker compose restart sso-service
```

### Installing dependencies

- requires Python 3.11 + pip;

```shell
> python -m venv .venv
> source ./.venv/Script/activate  # Windows
> source ./.venv/bin/activate  # Linux
> pip install -r ./requirements/default.txt
```

### Migration generation

```shell
> source ./.venv/Script/activate  # Windows
> source ./.venv/bin/activate  # Linux
> alembic -c src/traveling_sso/database/alembic.ini revision --autogenerate -m "<comment>"
> docker compose restart sso-service
```
