#!/bin/bash
set -o allexport
source ./env/dev.env
set +o allexport

python manage.py migrate
python manage.py setup_project