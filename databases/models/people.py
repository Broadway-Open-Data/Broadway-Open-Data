from databases import db, models

import datetime

from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

# import custom stuff
from nameparser import HumanName



# --------------------------------------------------------------------------------



class ShowsRolesLink(db.Model):
    __tablename__ = 'shows_roles_link'
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    extra_data = db.Column(db.String(256))





# I might not need this association table...
# A table for person, shows, and roles
# roles_table = db.Table('roles_table',
#         db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, models.dbTable):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=True)
    type = db.Column(db.String(40), unique=False, nullable=True)
    url = db.Column(db.String(120), unique=False, nullable=True)
    description = db.Column(db.String(255), unique=False, nullable=True)

    # models
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

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

race_table = db.Table('racial_identity_lookup_table',
        db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
        db.Column('racial_identity_id', db.Integer(), db.ForeignKey('racial_identity.id')))


class RacialIdentity(db.Model, models.dbTable):
    __tablename__ = "racial_identity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

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


    name_title =  db.Column(db.String(10), nullable=True, unique=False)
    f_name = db.Column(db.String(40), nullable=False, unique=False)
    m_name = db.Column(db.String(40), nullable=True, unique=False)
    l_name = db.Column(db.String(40), nullable=False, unique=False)
    name_suffix = db.Column(db.String(10), nullable=True, unique=False)
    name_nickname = db.Column(db.String(40), nullable=True, unique=False)

    @hybrid_property
    def full_name(self):
        """Return proper casing too"""
        name_string = " ".join(list(filter(None, [self.name_title, self.f_name, self.m_name, self.l_name, self.name_suffix, self.name_nickname])))
        full_name = HumanName(name_string)
        full_name.capitalize()
        return full_name


    url = db.Column(db.String(120), unique=False, nullable=True)
    #  Date of birth (or something blurred).
    date_of_birth = db.Column(db.DateTime, nullable=True)



    # --------------------------------------------------------------------------
    # Here's where I need help with...
    gender_identity_id = db.Column(db.Integer, db.ForeignKey('gender_identity.id'))
    gender_identity = db.relationship('GenderIdentity', backref="person")

    # --------------------------------------------------------------------------

    # one to many
    # roles = db.relationship('Role', secondary=roles_table, backref=db.backref('person', lazy='dynamic'), passive_deletes=True)
    roles = relationship('Role', secondary='shows_roles_link', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)
    shows = relationship('Show', secondary='shows_roles_link', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)

    racial_identity = db.relationship('RacialIdentity', secondary='racial_identity_lookup_table', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)


    # Additional fields
    country_of_birth = db.Column(db.String(40), nullable=True, unique=False)
    fluent_languages = db.Column(db.String(80), nullable=True, unique=False)


    # Assert is lowercase
    @validates('f_name', 'm_name', 'l_name', 'full_name', 'country_of_birth', 'fluent_languages')
    def convert_lower(self, key, value):
        if isinstance(value, str):
            return value.lower()
        else:
            return value











#
