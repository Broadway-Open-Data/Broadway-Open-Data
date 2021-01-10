import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ConnectDb:
    def __init__(self, **kwargs):
        self.DB_URI = kwargs.get('DB_URI', os.environ.get('DB_URI', 'mysql+pymysql://root:broadway@localhost:3306/broadway'))
        self.engine = create_engine(self.DB_URI)

        # You can technically have multiple db uris and engines, but we won't be doing that here..

        # initialize this as null
        self._session = None
    # --------------------------------------------------------------------------

    # Create a new session...
    @property
    def session(self):
        """
        Lazy load a session. The session doesn't exist until the `self.session` command is called.

        To access the "main session" execute the following:
        >> session = self.session

        To create a new session (useful for multiprocessing):
        >> session = self._create_session()

        ----
        For more details on sessions, read here: https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
        """
        if not self._session:
            self._session = self._create_session()

        return self._session


    # Session maker
    def _create_session(self):
        """
        This command explicitly creates a new session by calling the sessionmaker.
            ... Synonymous with `sessionmaker(bind=self.engine)`

        NOTE: Use carefully.
        """
        return sessionmaker(bind=self.engine)
