from sqlalchemy import create_engine
import sqlalchemy
import os
# import mysql
import pymysql

drivername="mysql"
host = "open-broadway-data.cnti8o0ilvhg.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "shows"
dbInstanceIdentifier = "open-broadway-data"
username = os.environ.get("RDS_USERNAME")
password = os.environ.get("RDS_PASSWORD")


print(password,"\n\n")
# make the url to be used for the sql engine
engine_url = sqlalchemy.engine.url.URL(
    drivername,
    username=username,
    password=password,
    host=host,
    port=port,
    database=dbname
    )

engine = create_engine(engine_url)

# This isn't working...
# conn = pymysql.connect(
#     host=host,
#     user=username,
#     passwd=password,
#     port=port,
#     db=dbname,
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
#     )
#
# cur = conn.cursor()
