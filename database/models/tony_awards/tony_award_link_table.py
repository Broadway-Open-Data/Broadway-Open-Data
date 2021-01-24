import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import YEAR

from sqlalchemy.orm import validates


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# --------------------------------------------------------------------------------


class TonyAwardLink(Base, BaseTable):

    __tablename__ = 'tony_award_link'
    __table_args__ = {
        'comment': 'This table represents a tony award instance. (Example: Best Lighting Design for a Musical.)'
    }


    id = Column(Integer, primary_key=True)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # relationship fields
    award_id = Column(Integer, ForeignKey('tony_award.id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), index=True, nullable=True)
    show_id = Column(Integer, ForeignKey('show.id'), index=True, nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'), index=True, nullable=True)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # Internally managed
    date_awarded = Column(YEAR, nullable=False, comment='When was this award awarded?')

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


    def __repr__(self):
        return f"{self.id}: {self.name}"
