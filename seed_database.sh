#!/bin/bash

rm db.sqlite3
rm -rf ./pixoapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pixoapi
python3 manage.py migrate pixoapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata pixousers
python3 manage.py loaddata images
python3 manage.py loaddata collectibles
python3 manage.py loaddata categories
python3 manage.py loaddata collectiblecategories
python3 manage.py loaddata imagegalleries