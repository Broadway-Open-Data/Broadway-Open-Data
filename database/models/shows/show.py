import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from sqlalchemy.sql import expression
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

# mysql specific columns
from sqlalchemy.dialects.mysql import TINYINT, YEAR


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# ------------------------------------------------------------------------------

class Show(Base, BaseTable):
    """
    A table representing a broadway show.
    """
    __tablename__ = 'show'

    id = Column(Integer, primary_key=True)
    date_instantiated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment='internally managed')

    # the basics
    title = Column(String(200), nullable=True)
    opening_date = Column(DateTime, nullable=True, index=True)
    closing_date = Column(DateTime, nullable=True, index=True)
    previews_date = Column(DateTime, nullable=True)
    year = Column(YEAR, index=True, nullable=True) # I'd prefer to have this stored as a datetime?

    # theatre
    theatre_id = Column(Integer, ForeignKey('theatre.id'), nullable=True, index=True)
    scraped_theatre_name = Column(String(60), index=False, nullable=True)


    # types
    production_type = Column(String(20), nullable=True) # Convert to a join table
    show_type = Column(String(20), nullable=True)
    show_type_simple = Column(String(20), nullable=True)


    # numerics
    intermissions = Column(TINYINT, nullable=True)
    n_performances = Column(Integer, nullable=True)
    run_time = Column(Integer, nullable=True)

    # booleans
    show_never_opened = Column(Boolean, server_default=expression.true(), nullable=False)
    revival = Column(Boolean, server_default=expression.true(), nullable=False)
    pre_broadway = Column(Boolean, server_default=expression.true(), nullable=False)
    limited_run = Column(Boolean, server_default=expression.true(), nullable=False)
    repertory = Column(Boolean, server_default=expression.true(), nullable=False)


    # Other stuff
    other_titles = Column(String(300), nullable=True, comment="should this be made into an association table?")
    official_website = Column(String(100), nullable=True, comment="this should be made into an associated table...")


    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # RELATIONSHIPS
    theatre = relationship('Theatre', backref='show', passive_deletes=True)
    theatre_name = association_proxy('theatre', 'theatre_name')



    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def __repr__(self):
        return f"{self.id}: {self.title} ({self.year})"
    # relationships – build this later...
    # @hybrid_property
    # def people(self):
    #     return models.ShowsRolesLink.query.filter(show_id=self.id).all()

# def foo(mapper, connection, target):
#     state = db.inspect(target)
#     changes = {}
#     print("foo")
#
