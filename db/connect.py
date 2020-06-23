import os
import json
import sys

# import pymysql
# import mysql
from sqlalchemy import create_engine
import sqlalchemy

sys.path.append(".")

# get the credentials
with open("secret/RSD_CREDENTIALS.json", "r") as f:
    creds = json.load(f)
    username = creds.get("RDS_USERNAME")
    password = creds.get("RDS_PASSWORD")

# Access the path and stuff
drivername="mysql+pymysql"
host = "open-broadway-data.cnti8o0ilvhg.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "shows"


# ===============================================================
# make the url to be used for the sql engine
connection_string = sqlalchemy.engine.url.URL(
    drivername=drivername,
    username=username,
    password=password,
    host=host,
    port=port,
    database=dbname
    )

# Connect
engine = create_engine(connection_string)

# BINGO!
print(engine.table_names())
