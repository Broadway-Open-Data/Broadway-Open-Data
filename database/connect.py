import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ConnectDb:
    def __init__(self, **kwargs):
        self.DB_URI = kwargs.get('DB_URI', os.environ.get('DB_URI', 'postgresql://yaakov:@localhost:5433/postgres'))
        self.engine = create_engine(self.DB_URI)

        # You can technically have multiple db uris and engines, but we won't be doing that here..
        self.Session = sessionmaker(bind=self.engine)

    # --------------------------------------------------------------------------

    # Create a new session...
    @property
    def session(self):
        """
        For more details on sessions, read here: https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
        """
        return self.Session()
