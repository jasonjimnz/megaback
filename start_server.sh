#!/bin/bash

echo "Running migrations"
python3 /megaback/manage.py migrate
echo "Running server"
python3 /megaback/manage.py runserver 0.0.0.0:8000

exit 0