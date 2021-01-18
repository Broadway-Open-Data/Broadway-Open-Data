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

# database models
from database.models.people.gender_identity import GenderIdentity

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

    # one to many
    roles = relationship('Role', secondary='shows_roles_link', backref=backref('person', lazy='dynamic'), passive_deletes=True)
    shows = relationship('Show', secondary='shows_roles_link', backref=backref('person', lazy='dynamic'), passive_deletes=True)

    # --------------------------------------------------------------------------

    # Create a relationship for racial identities
    _racial_identity = relationship(
        'RacialIdentity',
        secondary='racial_identity_association',
        backref=backref('person', lazy='dynamic'),
        passive_deletes=True
    )
    racial_identity = association_proxy('_racial_identity', 'name')

    # Create a relationship for gender identities
    _gender_identity = relationship(
        'GenderIdentity',
        secondary='gender_identity_association',
        backref=backref('person', lazy='dynamic'),
        passive_deletes=True
    )
    gender_identity = association_proxy('_gender_identity', 'name')

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

    def change_gender_identity(self, op, value):
        """
        Will update a person's gender identity. (This should work for racial identity too...)

        Params:
            op: (str) Operation. Either "equal" or "append"
                "equal" --> will assert that this person's gender identity matches provided value(s)
                "append" --> will add if this person's gender identity doesn't contain the provided value(s)
            value: (str|list) either a string or a list of values
        """
        # make sure the operation is valid
        assert op in ('equal', 'append')

        # if a string, convert to a tuple
        if isinstance(value, (str)):
            value = (value, )

        if op=='equal':
            for v in value:
                # add the gender identity
                if v not in self.gender_identity:
                    # Hacked get or create method
                    my_gender_id = GenderIdentity.get_by_attr('name', v.lower())
                    if not my_gender_id:
                        my_gender_id = GenderIdentity(name=v.lower())
                    self._gender_identity.append(my_gender_id)


        if self.gender_identity ==value:
            # Do nothing
            None
        else:
            my_gender = GenderIdentity.get_by_name(value)
            if not my_gender:
                my_gender = GenderIdentity(name=value)
                my_gender.save_to_db()

            # Now update
            self.update_info(update_dict={'gender_identity_id':my_gender.id})









#
