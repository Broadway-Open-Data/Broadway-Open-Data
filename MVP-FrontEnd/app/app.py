"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""
import os
import sys
# set the path to the root
sys.path.append(".")


import subprocess
import requests
import pandas as pd

from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

# Import forms
from forms.select_data import dataForm

# import utils
from utils.get_db_uri import get_db_uri

# Import cache
from common.extensions import cache


# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)

# Configure the app
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

# Create a session for querying sql
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session(autoflush=False)


# Build tables
shows = Table('shows', metadata, autoload=True)
theatres = Table('theatres', metadata, autoload=True)

# Connect the db to the app
# db.init_app(app)
# with app.app_context():
#     db.create_all()


# Now build the connection


# ==============================================================================
# Build routes
# ==============================================================================



# Home
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------

# Allow the user to request specific data from the app
@app.route('/submit-data/',  methods=['GET', 'POST'])
def submit_data():

    form = dataForm(request.form)

    if request.method == 'POST':
        if True: #form.validate():
            my_data = {}
            for key, value in form.allFields.data.items():
                if type(value)==dict:
                    my_data.update(value)
            # get rid of the csrf token
            del my_data["csrf_token"]

            cache.set("user_query",my_data)

            return redirect('/submit-data-success/')
    else:
        return render_template('submit-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------

# Submitted query
@app.route('/submit-data-success/',  methods=['GET'])
def submit_data_success():

    data = cache.get("user_query")

    # Success vs. Failure
    if data:
        # Omit all empty keys
        # data = {k:v for k,v in data.items() if v not in ["", None]}

        get_selected = lambda arr: [x for x in arr if data.get(x)]
        show_type = get_selected(["musicals","plays","other_show_genre"])
        production_type = get_selected(["originals","revivals","other_production_type"])

        show_title = data.get("title")
        show_keyword = data.get("keyword")
        show_id = data.get("showId")

        theatre_name = data.get("theatreName")
        theatre_id = data.get("theatreId")

        # 1. Query db by start and end date
        start_dt = data.get("startDate")
        end_dt = data.get("endDate")

        #  *  *  *  *  *  *  *  *  *  *  *  *
        #  This is where the magic happens
        #  Make the query here...
        #  *  *  *  *  *  *  *  *  *  *  *  *

        # return jsonify(prediction)
        return render_template('submit-data-success.html', title="Success", data=data)
    else:
        return render_template('submit-data-failure.html', title="Failure")



# ------------------------------------------------------------------------------

@app.route('/return-data/', methods=['GET','POST'])
def return_data():
    """submit a specific json, returns data"""

    # Retrieve the data from  user's request
    data = cache.get("user_query")

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # (Copied from above)
    # 1. Query db by start and end date
    start_dt = data.get("startDate")
    end_dt = data.get("endDate")

    #  *  *  *  *  *  *  *  *  *  *  *  *
    #  This is where the magic happens
    #  Make the query here...
    query_shows = session.query(shows).filter(shows.year>=1900)
    df = pd.DataFrame(query_shows)

    #  *  *  *  *  *  *  *  *  *  *  *  *

    # Return the response in json format
    return render_template('return-data.html', data = data)



# ------------------------------------------------------------------------------


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", debug=True)
