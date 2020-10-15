from databases import db, models
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy.sql import expression
from sqlalchemy.ext.hybrid import hybrid_property

import datetime


# ------------------------------------------------------------------------------

class DataEdits(db.Model, models.dbTable):
    """"""
    __tablename__ = "data_edits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # can be used to groupby...
    edit_id = db.Column(db.Integer, nullable=False, unique=False, primary_key=True)
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # edit details
    table_name = db.Column(db.String(80), nullable=False, unique=False)
    value_primary_id = db.Column(db.Integer, nullable=False, unique=False) # This is the row referred to in the edit..

    field = db.Column(db.String(40), nullable=False, unique=False)
    field_type = db.Column(db.String(40), default="VARCHAR(40)", nullable=False, unique=False)
    value_pre = db.Column(db.String(300), nullable=True, unique=False)
    value_post = db.Column(db.String(300), nullable=False, unique=False)

    # Who made the edit ?
    edit_by = db.Column(db.String(40), nullable=False, unique=False)
    edit_comment = db.Column(db.String(300), nullable=True, unique=False)
    edit_citation = db.Column(db.String(200), nullable=True, unique=False)

    # who approved the edit?
    approved = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    approved_by = db.Column(db.String(40), nullable=False, unique=False)
    approved_comment = db.Column(db.String(300), nullable=True, unique=False)

    # the basics
