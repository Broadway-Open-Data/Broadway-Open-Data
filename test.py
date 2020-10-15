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

    x = models.Show().query.order_by('opening_date').first()

    # update the value
    new_website = 'http://https//americanutopiabroadway.com/'
    update_dict = {'official_website':new_website}
    x.update_info({'official_website':new_website})


    # print(x)
