from databases import models

# x = models.Person(
#     f_name="James",
#     m_name="F.",
#     l_name="Buckley"
# )
#
# print(x.gender_identity)
# print("*"+x.full_name+"*")
#
#
# for c in models.Person.__table__.columns:
#     print(c.type)


# ------------------------------------------------------------------------------
from flask import Flask
from databases.db_uri import get_db_uri
from databases import db

# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():

    # Get a show and update it...
    x = models.Person.query.filter_by(url = '/people/Lin-Manuel-Miranda/').first()

    print(f"""
    {x.full_name=}
    {x.gender_identity=}
    {x.racial_identity=}
    {x.roles=}
    {x.shows=}
    """)

    # update the value
    # new_website = 'https://inresidenceonbroadway.com/'
    # update_dict = {'official_website':new_website}
    # x.update_info(update_dict={'official_website':new_website})
