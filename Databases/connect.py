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
# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

    # ------------------------------------------------------------------------------

    # Now load the data
    df = pd.read_csv("data/all_show_info_cleaned.csv")

    cols = ['Title', 'Opening Date', 'Theatre ID', 'Theatre Name (from Show Info)',
       'Production Type', 'Intermissions', 'Show Type', 'Show ID', 'Year',
       'Closing Date', 'N Performances', 'Other Titles', 'Previews Date',
       'Running Time', 'Official Website', 'Show Type Simple',
       'Show Never Opened', 'Run Time', 'Revival', 'Pre-Broadway',
       'Limited Run', 'Repertory']

    sql_cols = [column.key for column in Show.__table__.columns]
    sql_cols = Show.__table__.columns.keys()

    # Match up these columns with each other...
    cols = df.columns.str.lower().str.replace("-","_").str.replace(" ","_")
    for x in cols:
        if x not in sql_cols:
            print(x)
    # Then add them to the db!
    # ['id', 'date_instantiated', 'title', 'opening_date', 'closing_date', 'previews_date', 'year', 'theatre_id', 'theatre_name', 'production_type', 'show_type', 'show_type_simple', 'intermissions', 'n_performances', 'running_time', 'show_never_opened', 'revival', 'pre_broadway', 'limited_run', 'repertory', 'other_titles', 'official_website']

    # print(cols)
    # # Do these things now.. .
    # now = datetime.datetime.utcnow()
    #
    # my_show = Show(
    #     id=str(uuid.uuid4()),
    #     date_instantiated=now,
        # title=row.get("Title"),
    # )
    # db.session.add(my_show)
    # del my_show
    #
    # my_theatre = Theatre(
    #     id=str(uuid.uuid4()),
    #     date_instantiated=now,
    # )
    # db.session.add(my_theatre)
    # del my_theatre
    # db.session.commit()
