#!/bin/bash

rm db.sqlite3
rm -rf ./pixoapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pixoapi
python3 manage.py migrate pixoapi
python3 manage.py loaddata categories
python3 manage.py loaddata conditions
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata pixousers