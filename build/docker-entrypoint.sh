#!/bin/bash

set -e

alembic -c src/traveling_sso/database/alembic.ini upgrade head

python bin/run.py
