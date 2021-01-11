import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import TEXT

from sqlalchemy.sql import expression
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

# import specialized modules
from nameparser import HumanName


# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# ------------------------------------------------------------------------------

class DataEdits(Base, BaseTable):
    """
    A table representing all edits made.
    """

    __tablename__ = "data_edits"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # can be used to groupby...
    edit_id = Column(Integer, nullable=False, unique=False, primary_key=True)
    edit_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # edit details
    table_name = Column(String(80), nullable=False, unique=False)
    value_primary_id = Column(Integer, nullable=False, unique=False) # This is the row referred to in the edit..

    field = Column(String(40), nullable=False, unique=False)
    field_type = Column(String(40), default="VARCHAR(40)", nullable=False, unique=False)
    value_pre = Column(TEXT, nullable=True, unique=False)
    value_post = Column(TEXT, nullable=False, unique=False)

    # Who made the edit ?
    edit_by = Column(String(60), nullable=False, unique=False)
    edit_comment = Column(TEXT, nullable=True, unique=False)
    edit_citation = Column(String(200), nullable=True, unique=False)

    # who approved the edit?
    approved = Column(Boolean, server_default=expression.false(), nullable=False)
    approved_by = Column(String(60), nullable=False, unique=False)
    approved_comment = Column(TEXT, nullable=True, unique=False)

    # the basics
