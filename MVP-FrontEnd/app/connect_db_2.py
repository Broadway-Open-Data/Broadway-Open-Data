import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append(".")

import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import or_

# import utils
from utils.get_db_uri import get_db_uri

# ------------------------------------------------------------------------------

# Use this resource https://www.pythonsheets.com/notes/python-sqlalchemy.html

# Now build the connection
SQLALCHEMY_DATABASE_URI = get_db_uri()
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
conn = engine.connect()


# bind and reflect
metadata = MetaData()
metadata.reflect(bind=engine)

# Build your table
shows = metadata.tables['shows']
theatres = metadata.tables['theatres']

# select statement
select_st = select([shows]).where(
   shows.c.year == 1990)



# ------------------------------------------------------------------------------

# join statement
join_obj = shows.join(theatres, shows.c.theatre_id == theatres.c.id)

# Create the select statement
select_st =  select([shows, theatres]).where(
   shows.c.year == 1990).select_from(join_obj)

res = conn.execute(select_st)
for _row in res:
    print(_row)


# ------------------------------------------------------------------------------


# Make an SQL call
# result = engine.execute('SELECT * FROM shows;')
# print(result.fetchall())


# ------------------------------------------------------------------------------


# # Shows
# shows = Table('shows', metadata, autoload=True)
# query_shows = session.query(shows).all()
# df = pd.DataFrame(query_shows)
# print(df)
#
# # Theatres
# theatres = Table('theatres', metadata, autoload=True)
# query_theatres = session.query(theatres).all()
# df = pd.DataFrame(query_theatres)
# print(df)
