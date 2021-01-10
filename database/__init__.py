# from .session import *
from .connect import *

# Create your database connection here
# NOTE: if you want to parallelize this operation, you can create many sessions
# using the same code.
my_db_connection = ConnectDb()
session = my_db_connection.session

from .metadata import metadata

from . import methods
from . import models
