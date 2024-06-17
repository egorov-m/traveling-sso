#!/bin/bash

set -e

python manage.py create-user --default-root-admin
