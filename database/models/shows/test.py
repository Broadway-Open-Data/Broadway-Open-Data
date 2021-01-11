import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

# app stuff
from database.models.base import Base
from database.models.base_table import BaseTable


# ==============================================================================
#    X. Email
# ==============================================================================


class Foo(Base, BaseTable):
    """
    This is a test, just to see if things work
    """
    __tablename__ = 'foo'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)
    description = Column(String(255), unique=False, nullable=True)
