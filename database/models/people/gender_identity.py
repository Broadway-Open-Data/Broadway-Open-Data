import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.sql import expression
from sqlalchemy.orm import validates


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# --------------------------------------------------------------------------------

class GenderIdentityAssociation(Base, BaseTable):
    __tablename__ = 'gender_identity_association'
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True, nullable=False)
    gender_identity_id = Column(Integer, ForeignKey('gender_identity.id'), primary_key=True, nullable=False)



class GenderIdentity(Base, BaseTable):
    __tablename__ = "gender_identity"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True, comment='constrain to lowercase values')
    description = Column(String(200), unique=False, nullable=True, comment='This field is optional.')

    # internally managed
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed.')
    date_updated = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow, comment='internally managed.')

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    def __repr__(self):
        return f"{self.id}: {self.name}"
