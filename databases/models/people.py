from databases import db, models

import datetime

from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

# import custom stuff





# --------------------------------------------------------------------------------

# Create roles
roles_table = db.Table('roles_table',
        db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, models.dbTable):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_last_edited = db.Column(db.DateTime, nullable=True)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()





# --------------------------------------------------------------------------------

race_table = db.Table('race_table',
        db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
        db.Column('racial_identity_id', db.Integer(), db.ForeignKey('racial_identity.id')))


class RacialIdentity(db.Model, models.dbTable):
    __tablename__ = "racial_identity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_last_edited = db.Column(db.DateTime, nullable=True)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()


# --------------------------------------------------------------------------------

class GenderIdentity(db.Model, models.dbTable):
    __tablename__ = "gender_identity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_last_edited = db.Column(db.DateTime, nullable=True)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()





# --------------------------------------------------------------------------


class Person(db.Model, models.dbTable):
    """"""
    __tablename__ = "person"
    id = db.Column(db.Integer,primary_key=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


    f_name = db.Column(db.String(40), nullable=False, unique=False)
    m_name = db.Column(db.String(40), nullable=True, unique=False)
    l_name = db.Column(db.String(40), nullable=False, unique=False)

    @hybrid_property
    def full_name(self):
        return " ".join(list(filter(None, [self.f_name, self.m_name, self.l_name])))


    #  Date of birth (or something blurred).
    date_of_birth = db.Column(db.DateTime, nullable=True)

    # one to many
    roles = db.relationship('Role', secondary=roles_table, backref=db.backref('person', lazy='dynamic'))

    # --------------------------------------------------------------------------
    # Here's where I need help with...
    # 1:1 relationship – Have to figure this out later...
    gender_identity = db.Column(db.String, nullable=False, db.ForeignKey('gender_identity.id'))

    # --------------------------------------------------------------------------

    # one to many
    racial_identity = db.relationship('RacialIdentity', secondary=race_table, backref=db.backref('person', lazy='dynamic'))


    # Additional fields
    country_of_birth = db.Column(db.String(40), nullable=True, unique=False)
    first_language = db.Column(db.String(40), nullable=True, unique=False)


    # Assert is lowercase
    @validates('f_name', 'm_name', 'l_name', 'full_name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods








#
