# sql alchemy
from sqlalchemy.ext.declarative import declarative_base
from database import metadata

Base = declarative_base(metadata=metadata)
