import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append(".")

# Internal stuff
from databases import db
from databases.models import Show, Theatre
from databases.db_uri import get_db_uri

# Flask stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Data tools
import pandas as pd
import numpy as np

# custom stuff
from databases.add_to_db import add_shows, query_all_shows, add_theatres
# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def do_all():

    with app.app_context():
        # Don't need this...
        # db.create_all()

        task_1 = True # manually toggle for now
        if task_1:

            # If you want to query all the show ids...
            all_show_ids = query_all_shows(db)

            # ------------------------------------------------------------------------------

            # Add shows
            add_shows(db)

            # ------------------------------------------------------------------------------

            # Add theatres
            add_theatres(db)


            print("*****\nDONE! All data is living in the database.\n*****")

        task_2 = False # manually toggle for now
        if task_2:
            my_show = Show.get_by_id(3)
            print(my_show)



if __name__ =='__main__':
    do_all()
