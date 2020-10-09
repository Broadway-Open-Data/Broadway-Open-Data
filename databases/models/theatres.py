from databases import db, models

import datetime


class Theatre(db.Model, models.dbTable):
    """"""
    __tablename__ = "theatres"
    id = db.Column(db.Integer, primary_key=True, nullable=False, default=0, unique=True, index=True)
    date_instantiated = db.Column(db.DateTime,  nullable=False, default=datetime.datetime.utcnow)

    # the basics
    theatre_name = db.Column(db.String(200), nullable=True)
    street_address = db.Column(db.String(200), nullable=True)
    address_locality = db.Column(db.String(100), nullable=True)
    address_region = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)

    # date stuff
    year_closed = db.Column(db.Integer, nullable=True)
    year_demolished = db.Column(db.Integer, nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
