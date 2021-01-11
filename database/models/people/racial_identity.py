import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import TEXT, YEAR

from sqlalchemy.sql import expression
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

# import specialized modules
from nameparser import HumanName

# mysql specific columns
from sqlalchemy.dialects.mysql import TINYINT, YEAR


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# --------------------------------------------------------------------------------

class RacialIdentityAssociation(Base):
    __tablename__ = "racial_identity_association"
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True, nullable=False)
    racial_identity_id = Column(Integer, ForeignKey('racial_identity.id'), primary_key=True, nullable=False)


class RacialIdentity(Base, BaseTable):
    __tablename__ = "racial_identity"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True, comment='constrain to lowercase values')
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
