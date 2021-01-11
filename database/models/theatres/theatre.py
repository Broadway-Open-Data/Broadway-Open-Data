import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

# mysql specific columns
from sqlalchemy.dialects.mysql import TINYINT, YEAR


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# ------------------------------------------------------------------------------

class Theatre(Base, BaseTable):
    """
    A table representing broadway theatres.

    NOTE: work is needed to match theatres which change names...
    """
    __tablename__ = 'theatre'


    id = Column(Integer, primary_key=True)
    date_instantiated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed')

    # the basics
    theatre_name = Column(String(200), nullable=True)
    street_address = Column(String(300), nullable=True)
    address_locality = Column(String(100), nullable=True)
    address_region = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)

    # date stuff
    year_closed = Column(YEAR, nullable=True)
    year_demolished = Column(YEAR, nullable=True)
    capacity = Column(Integer, nullable=True)
