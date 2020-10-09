import json


class dbTable():
    """
    Base class for all objects in a table
    """


    # Lookup by id
    @classmethod
    def get_by_id(self, id):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(id=id).first()

    # Method to save role to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove role from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Udate info
    def update_info(self, update_dict):
        self.query.filter_by(id=self.id).update(update_dict, synchronize_session=False)
        self.save_to_db()


    # Define string methods...
    def __data__(self):
        data = {x: getattr(self, x) for x in self.__mapper__.columns.keys()}
        # data = {x: str(getattr(self, x)) for x in self.__mapper__.columns.keys()}
        return data

    def __str__(self):
        data = self.__data__()
        return json.dumps(data, default=str)
