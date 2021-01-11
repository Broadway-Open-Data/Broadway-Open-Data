import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
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



class ShowsRolesLink(Base, BaseTable):
    """
    This table defines which people worked on which shows in which roles.

    ----

    Some sanity checks:
        * a person can work on many shows
        * a person in one show can have multiple roles
        * a show can have many people with the same role

    """
    __tablename__ = 'shows_roles_link'

    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    show_id = Column(Integer, ForeignKey('show.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    extra_data = Column(TEXT, comment='Allow text of unlimited length')
    url = Column(String(200), unique=False, nullable=True, comment='This field is optional.')



# I might not need this association table...
# A table for person, shows, and roles
# roles_table = Table('roles_table',
#         Column('person_id', Integer(), ForeignKey('person.id')),
#         Column('role_id', Integer(), ForeignKey('role.id')))


class Role(Base, BaseTable):
    """
    A table representing a possible job titles ("roles") for working on a Broadway show.
    """

    __tablename__ = 'role'


    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False, comment='constrain to lowercase values') # All actors will be classified as "Performer"
    description = Column(String(200), unique=False, nullable=True, comment='This field is optional.')

    # models
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed.')
    date_updated = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow, comment='internally managed.')


    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()


    # # Methods
    # @classmethod
    # def get_by_name(self, name):
    #     """Get the id, name, description of a role based on the role name"""
    #     return self.query.filter_by(name=name).first()

    def __repr__(self):
        return f"{self.id}: {self.name}"


# --------------------------------------------------------------------------------

race_table = Table('racial_identity_lookup_table',
        Column('person_id', Integer(), ForeignKey('person.id')),
        Column('racial_identity_id', Integer(), ForeignKey('racial_identity.id')))


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

# --------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------


class Person(Base, BaseTable):
    """
    A table representing a person. (These are people who've work on a Broadway show.)
    """
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)


    # internally managed
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed.')
    date_updated = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow, comment='internally managed.')

    # Break a name down to its pieces...
    name_title =  Column(String(10), nullable=True, unique=False)
    f_name = Column(String(40), nullable=True, unique=False)
    m_name = Column(String(40), nullable=True, unique=False)
    l_name = Column(String(40), nullable=True, unique=False)
    name_suffix = Column(String(10), nullable=True, unique=False)
    name_nickname = Column(String(40), nullable=True, unique=False)

    # Perhaps store this as a real attribute and update using events?
    @hybrid_property
    def full_name(self):
        """Return proper casing too"""
        name_string = " ".join(list(filter(None, [self.name_title, self.f_name, self.m_name, self.l_name, self.name_suffix, self.name_nickname])))
        full_name = HumanName(name_string)
        full_name.capitalize()
        return str(full_name)


    # This is probably better stored in its own table...
    broadway_world_url = Column(String(120), unique=False, nullable=True, comment='This person\'s url on broadwayworld.com')

    #  Date of birth (or something blurred).
    date_of_birth = Column(DateTime, nullable=True)
    year_of_birth = Column(YEAR, nullable=True)

    # Additional fields
    country_of_birth = Column(String(40), nullable=True, unique=False)
    fluent_languages = Column(String(80), nullable=True, unique=False)


    # --------------------------------------------------------------------------
    # Need to revisit these relationships

    gender_identity_id = Column(Integer, ForeignKey('gender_identity.id'))
    gender_identity = relationship('GenderIdentity', backref="person")

    # --------------------------------------------------------------------------

    # one to many
    # roles = relationship('Role', secondary=roles_table, backref=backref('person', lazy='dynamic'), passive_deletes=True)
    roles = relationship('Role', secondary='shows_roles_link', backref=backref('person', lazy='dynamic'), passive_deletes=True)
    shows = relationship('Show', secondary='shows_roles_link', backref=backref('person', lazy='dynamic'), passive_deletes=True)

    racial_identity = relationship(
        'RacialIdentity',
        secondary='racial_identity_lookup_table',
        backref=backref('person', lazy='dynamic'),
        passive_deletes=True
    )


    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # VALIDATION

    @validates('f_name', 'm_name', 'l_name', 'full_name', 'country_of_birth', 'fluent_languages')
    def convert_lower(self, key, value):
        if isinstance(value, str):
            return value.lower()
        else:
            return value


    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # DATA EDITS

    # def edit_gender_identity(self, value):
    #
    #     if self.gender_identity ==value:
    #         # Do nothing
    #         None
    #     else:
    #         my_gender = GenderIdentity.get_by_name(value)
    #         if not my_gender:
    #             my_gender = GenderIdentity(name=value)
    #             my_gender.save_to_db()
    #
    #         # Now update
    #         self.update_info(update_dict={'gender_identity_id':my_gender.id})









#
