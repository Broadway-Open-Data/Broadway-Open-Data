import os
from pathlib import Path
import datetime
from sqlalchemy_schemadisplay import create_schema_graph

# my stuff
from database import metadata

def get_db_ERD(save_path=None, DB_URI=None):

    # If no save path, set it...
    if not save_path:
        dt_now = datetime.datetime.now()
        save_path = Path(f'database/dump/databases-ERD/style_{style} – {dt_now}.png')

    # Make the dir if you need to
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    graph = create_schema_graph(
        metadata=metadata,
        show_datatypes=True,
        show_indexes=True,
        rankdir='TB', # From left to right (instead of top to bottom)
        concentrate=True, # Don't try to join the relation lines together
        )

    graph.write_png(save_path)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -



if __name__=='__main__':

    get_db_ERD(DB_URI=os.environ.get('DB_URI','mysql+pymysql://root:broadway@localhost:3306/broadway'))






#
