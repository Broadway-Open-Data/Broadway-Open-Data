import json
import datetime
from databases import db
from databases import models

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
        self.before_update(update_dict)
        self.query.filter_by(id=self.id).update(update_dict, synchronize_session=False)
        self.save_to_db()


    # Define string methods...
    def __data__(self):
        data = {x: getattr(self, x) for x in self.__mapper__.columns.keys()}
        return data

    def __str__(self):
        data = self.__data__()
        return json.dumps(data, default=str)


    @classmethod
    def find_type(self, colname):
        if hasattr(self, '__table__') and colname in self.__table__.c:
            return self.__table__.c[colname].type
        for base in self.__bases__:
            return find_type(base, colname)
        raise NameError(colname)



    # @classmethod
    def before_update(self, update_dict):

        # Consult this to get the column dtypes?
        # state = db.inspect(self)


        edit_date = datetime.datetime.utcnow()
        # Get the edit id
        edit_id = db.session.query(models.DataEdits.edit_id).order_by(-models.DataEdits.edit_id.desc()).first()

        # autoincrement
        if edit_id:
            edit_id +=1
        else:
            edit_id = 1

        # Who made the edit ? – This will have to be built as a wrapper I guess...
        edit_by = '__obd_application__'
        approved = True
        approved_by = '__obd_application__'
        approved_comment = 'Automated edit made through the open broadway data backend interface.'

        # Get reference stuff
        table_name = self.__tablename__

        # Get the data
        _data = self.__data__()

        for key, value in update_dict.items():
            my_edit = models.DataEdits(
                edit_date=edit_date,
                edit_id=edit_id,
                edit_by=edit_by,
                approved=approved,
                approved_by=approved_by,
                approved_comment=approved_comment,
                table_name=table_name,
                field = key,
                field_type = self.find_type(key),
                value_pre = _data[key],
                value_post = value
            )
            print(my_edit)






# id = db.Column(db.Integer, primary_key=True)
# # can be used to groupby...
# edit_id = db.Column(db.Integer, nullable=False, unique=False)
# edit_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#
# # edit details
# table_name = db.Column(db.String(80), nullable=False, unique=False)
# field = db.Column(db.String(40), nullable=False, unique=False)
# field_type = db.Column(db.String(40), default="VARCHAR(40)", nullable=False, unique=False)
# value_pre = db.Column(db.String(300), nullable=True, unique=False)
# value_post = db.Column(db.String(300), nullable=False, unique=False)
#
# # Who made the edit ?
# edit_by = db.Column(db.String(40), nullable=False, unique=False)
# edit_comment = db.Column(db.String(300), nullable=True, unique=False)
# edit_citation = db.Column(db.String(200), nullable=True, unique=False)
#
# # who approved the edit?
# approved = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
# approved_by = db.Column(db.String(40), nullable=False, unique=False)
# approved_comment = db.Column(db.String(300), nullable=True, unique=False)










#
