from json import dump as jdump
from os import environ
from os.path import dirname, join

from yaml import dump as ydump

environ["INIT_ROOT_ADMIN_USER"] = "False"
environ["DB_POOL_PRE_PING"] = "False"

from traveling_sso.main import app


spec = app.openapi()

with open(join(dirname(__file__), "openapi.yaml"), "w") as f:
    ydump(spec, f)

with open(join(dirname(__file__), "openapi.json"), "w") as f:
    jdump(spec, f)
