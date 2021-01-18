import datetime
from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy.sql import expression
from sqlalchemy.orm import validates


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# --------------------------------------------------------------------------------


class Role(Base, BaseTable):
    """
    A table representing a possible job titles ("roles") for working on a Broadway show.
    """

    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, comment='constrain to lowercase values. Note: all actors will be classified as "Performer"')
    description = Column(String(200), unique=False, nullable=True, comment='This field is optional.')

    # models
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed.')
    date_updated = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow, comment='internally managed.')


    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    def __repr__(self):
        return f"{self.id}: {self.name}"
