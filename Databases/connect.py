import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append(".")


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Databases.db import db , Show, Theatre
from Databases.db_uri import get_db_uri

import pandas as pd
import numpy as np

# custom stuff
from Databases.add_to_db import add_shows, query_all_shows, add_theatres
# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

    # If you want to query all the show ids...
    all_show_ids = query_all_shows(db)

    # ------------------------------------------------------------------------------

    # Add shows
    add_shows(db)

    # ------------------------------------------------------------------------------

    # Add theatres
    add_theatres(db)


print("*****\nDONE! All data is living in the database.\n*****")
