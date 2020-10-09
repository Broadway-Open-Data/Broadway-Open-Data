#!/bin/bash
if [ ! -d "./migrations" ]
then
    echo "Creating the migrations directory."
    python3 databases/manage.py db init
fi

# python3 databases/manage.py db stamp head
python3 databases/manage.py db upgrade
python3 databases/manage.py db migrate
# python3 databases/manage.py db merge
