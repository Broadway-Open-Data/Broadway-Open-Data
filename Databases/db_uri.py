import os
import json
import sqlalchemy
import sys

# set the path to the root
sys.path.append(".")

# ------------------------------------------------------------------------------
# get the credentials
with open("secret/RSD_CREDENTIALS.json", "r") as f:
    creds = json.load(f)
    username = creds.get("RDS_USERNAME")
    password = creds.get("RDS_PASSWORD")


# Access the path and stuff
drivername="mysql+pymysql"
host = "open-broadway-data.cmftsskrmemn.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "broadway"


# ------------------------------------------------------------------------------
# make the url to be used for the sql engine
connection_string = sqlalchemy.engine.url.URL(
    drivername=drivername,
    username=username,
    password=password,
    host=host,
    port=port,
    database=dbname
    )
def get_db_uri():
    """returns the uri for connecting to the db"""
    return connection_string
# ------------------------------------------------------------------------------
