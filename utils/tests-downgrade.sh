#!/bin/bash

set -e

if alembic -c src/traveling_sso/database/alembic.ini current | grep -q head; then
    echo "Downgrade database.";
    alembic -c src/traveling_sso/database/alembic.ini downgrade base;
else
  echo "Downgrade database isn't necessary.";
fi
