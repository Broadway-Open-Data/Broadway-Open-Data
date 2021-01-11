import os
import json
import datetime
from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.exc import IntegrityError
# from sqlalchemy import Column, Integer, String
from sqlalchemy import inspect

# from database import models
from database.models.base import Base
# from database.models import DataEdits


from database import session



class BaseTable():
    """
    Base class for all objects in a table
    """


    # --------------------------------------------------------------------------

    # Access a session (to interact with the db)
    @property
    def session(self):
        """might need to rename this..."""
        return inspect(self).session



    # --------------------------------------------------------------------------
    # String methods

    # Define string methods...
    def __data__(self):
        data = {x: getattr(self, x) for x in self.__mapper__.columns.keys()}
        return data

    def __str__(self):
        data = self.__data__()
        return json.dumps(data, default=str)

    def as_dict(self):
        """This method calls all data directly related to `self`, relationships are ignored..."""
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result

    # --------------------------------------------------------------------------
    # Internal methods

    @classmethod
    def find_type(self, attr):
        # Get the attr from the table
        if hasattr(self, '__table__') and attr in self.__table__.c:
            return self.__table__.c[attr].type
        # If you couldn't find it in the table, get it from the class
        elif hasattr(self, attr):
            return type(getattr(self, attr))
        # Search through all the declared bases of the object (when used in multiple binds)
        for base in self.__bases__:
            return find_type(base, colname)

        # If nothing was found...
        raise NameError(colname)


    # --------------------------------------------------------------------------
    # Database methods


    # Lookup by attr
    @classmethod
    def get_by_attr(self, attr, value):
        """
        Get the an entity based on the first match of a give attribute.

        Ex: get('full_name','Brad Pitt')
            returns --> get first instance of Brad Pitt (or None)
        """

        return self.session.query(self).filter(getattr(self, attr)==value).first()


    # Method to save role to DB
    def save_to_db(self, raise_errors=True, verbose=True):
        """
        Will try to save to db. If it can't, will either raise errors and halt. Or continue.

        Wanted features:
            - asynchronous commit
            - will `self.session` work? Or should we pass `session` into the function
            - Answer: `session = inspect(self).session`
        """

        try:
            self.session.commit()

        # Rollback if there's an error
        except IntegrityError as err:
            self.session.rollback()

            if raise_errors:
                raise IntegrityError

            if verbose:
                print(f"{err}")


    # Method to remove role from DB
    def remove_from_db(self):
        self.session.delete(self)
        self.session.commit()


    # Udate info
    def update_info(self, **kwargs):
        # self.before_update(**kwargs)
        self.query.get(self.id).update(kwargs.get('update_dict'), synchronize_session=False)
        self.save_to_db()



    # --------------------------------------------------------------------------
    # Save updates

    # def before_update(self, **kwargs):
    #
    #     # Consult this to get the column dtypes?
    #     # state = db.inspect(self)
    #
    #
    #     # Get edit meta info
    #     edit_date = datetime.datetime.utcnow()
    #     edit_id = db.session.query(models.DataEdits.edit_id).order_by(-models.DataEdits.edit_id.asc()).first()
    #
    #     # Unpack the tuple to a result
    #     if edit_id:
    #         edit_id = edit_id[0] + 1
    #     else:
    #         edit_id = 1
    #
    #
    #     # Who made the edit ? – This will have to be built as a wrapper I guess...
    #     edit_by = kwargs.get('edit_by', '__obd_application__')
    #     edit_comment = kwargs.get('edit_comment', 'Automated edit made through the open broadway data backend interface.')
    #     approved =  kwargs.get('approved', True)
    #     approved_by = kwargs.get('approved_by', '__obd_application__')
    #     approved_comment = kwargs.get('approved_comment', 'Automated edit made through the open broadway data backend interface.')
    #
    #     # Get reference stuff
    #     table_name = self.__tablename__
    #
    #     # Get the data
    #     _data = self.__data__()
    #
    #
    #     for key, value in kwargs.get('update_dict').items():
    #
    #         # If no edit, then don't store
    #         if _data[key] == value:
    #             # No edit
    #             print("no edit needed")
    #             continue
    #
    #         my_edit = models.DataEdits(
    #             edit_date=edit_date,
    #             edit_id=edit_id,
    #             edit_by=edit_by,
    #             edit_comment=edit_comment,
    #             approved=approved,
    #             approved_by=approved_by,
    #             approved_comment=approved_comment,
    #             table_name=table_name,
    #             value_primary_id=self.id,
    #             field = key,
    #             field_type = str(self.find_type(key)),
    #             value_pre = _data[key],
    #             value_post = value
    #         )
    #         my_edit.save_to_db()












#
