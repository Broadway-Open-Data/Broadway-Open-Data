import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append(".")

import pandas as pd
import sqlalchemy

from sqlalchemy import Table, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

# import utils
from utils.get_db_uri import get_db_uri

# ------------------------------------------------------------------------------

# Now build the connection
SQLALCHEMY_DATABASE_URI = get_db_uri()

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session(autoflush=False)


# ------------------------------------------------------------------------------


# Shows
shows = Table('shows', metadata, autoload=True)
query_shows = session.query(shows).all()
df = pd.DataFrame(query_shows)
print(df)

# Theatres
theatres = Table('theatres', metadata, autoload=True)
query_theatres = session.query(theatres).all()
df = pd.DataFrame(query_theatres)
print(df)
