import datetime
from sqlalchemy import Column, Integer, String ForeignKey
from sqlalchemy.dialects.mysql import TEXT

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
