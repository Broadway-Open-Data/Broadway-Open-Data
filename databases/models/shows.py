from databases import db, models
from sqlalchemy.sql import expression
from uuid import uuid4
import datetime


# ------------------------------------------------------------------------------

class Show(db.Model, models.dbTable):
    """"""
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True, nullable=False, default=lambda: int(str(int(uuid.uuid4()))[:7]), unique=True, index=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # the basics
    title = db.Column(db.String(150), nullable=True)
    opening_date =  db.Column(db.DateTime, nullable=True)
    closing_date =  db.Column(db.DateTime, nullable=True)
    previews_date =  db.Column(db.DateTime, nullable=True)
    year = db.Column(db.Integer, index=True, nullable=True)

    # theatre
    theatre_id = db.Column(db.Integer, default=0, nullable=False)
    theatre_name = db.Column(db.String(40), index=False, nullable=True)

    # types
    production_type = db.Column(db.String(20), nullable=True)
    show_type = db.Column(db.String(20), nullable=True)
    show_type_simple = db.Column(db.String(20), nullable=True)

    # numerics
    intermissions = db.Column(db.Integer, nullable=True)
    n_performances = db.Column(db.Integer, nullable=True)
    run_time = db.Column(db.Integer, nullable=True)

    # booleans
    show_never_opened = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    revival = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    pre_broadway = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    limited_run = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    repertory = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    # Other stuff
    other_titles = db.Column(db.String(300), nullable=True)
    official_website = db.Column(db.String(40), nullable=True)
