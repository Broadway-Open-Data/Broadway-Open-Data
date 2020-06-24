import os
import json
import sys

# Correct the path
sys.path.append(".")

# Flask things
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# db things
from Databases.db import db
from Databases.db_uri import get_db_uri


# ------------------------------------------------------------------------------

# Instantiate a blank app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate the db
db.init_app(app=app)

# ------------------------------------------------------------------------------


# Instantiate the migration manager
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# ------------------------------------------------------------------------------

# # Create a hello world function
# @manager.command
# def hello(name=''):
#     print (f"hello {name}")
#
# # Create a create_all function
# @manager.command
# def create_all():
#     db.create_all()


# ------------------------------------------------------------------------------


if __name__ == '__main__':
    manager.run()
