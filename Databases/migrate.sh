#!/bin/bash
if [ ! -d "./migrations" ]
then
    echo "Creating the migrations directory."
    python3 Databases/manage.py db init
fi

# python3 Databases/manage.py db stamp head
python3 Databases/manage.py db upgrade
python3 Databases/manage.py db migrate
# python3 Databases/manage.py db merge
