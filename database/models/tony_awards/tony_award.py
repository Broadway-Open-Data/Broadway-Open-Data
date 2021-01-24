import datetime
from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy.orm import validates


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# --------------------------------------------------------------------------------


class TonyAward(Base, BaseTable):

    __tablename__ = 'tony_award'
    __table_args__ = {
        'comment': 'This table represents a tony award instance. (Example: Best Lighting Design for a Musical.)'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False, comment='The name of a Tony Award (this changes over time though...)')
    description = Column(String(300), unique=False, nullable=True, comment='This field is optional.')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # Internally managed
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed.')
    date_updated = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow, comment='internally managed.')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    
    def __repr__(self):
        return f"{self.id}: {self.name}"
