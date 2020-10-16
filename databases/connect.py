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
from databases import add_to_db
# add_shows, query_all_shows, add_theatres, add_people, add_people_and_roles
# ------------------------------------------------------------------------------


class ConnectApp():

    def __init__(self, **kwargs):

        # Instantiate a blank app
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # instantiate the db
        db.init_app(app=self.app)
        self.app.app_context().push()


    # ------------------------------------------------------------------------------

    # Create some methods

    def query_all_shows(self):
        """Get all existing show ids"""
        query_shows = db.session.query(Show.id).all()
        all_show_ids = [int(x[0]) for x in query_shows]
        return all_show_ids

    def query_all_theatres(self):
        """Get all existing show ids"""
        query_theatres = db.session.query(Theatre.id).all()
        all_theatre_ids = [int(x[0]) for x in query_theatres]
        return all_theatre_ids



#
# def do_all():
#
#
#             # If you want to query all the show ids...
#             all_show_ids = query_all_shows(db)
#
#             # ------------------------------------------------------------------------------
#
#             # Add shows
#             add_shows(db)
#
#             # ------------------------------------------------------------------------------
#
#             # Add theatres
#             add_theatres(db)
#
#
#             print("*****\nDONE! All data is living in the database.\n*****")
#
#         task_2 = True # manually toggle for now
#         if task_2:
#             # Add theatres
#             add_people(db)
#
#
#         task_3 = False # manually toggle for now
#         if task_3:
#             my_show = Show.get_by_id(3)
#             print(my_show)



if __name__ =='__main__':
    # do_all()
    db_app = ConnectApp()
    add_to_db.add_people_and_roles(db)
