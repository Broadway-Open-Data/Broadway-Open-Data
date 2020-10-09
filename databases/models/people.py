from .base import dbTable

# --------------------------------------------------------------------------

# Define models
# class RoleUsers(db.Table):
# roles_users = db.Table('roles_users',
#         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
#
#
# class Role(db.Model, RoleMixin, dbTable):
#     __tablename__ = "role"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))
#
#     # Show roles
#     def __repr__(self):
#         return '<User {}>'.format(self.id)
#
#     @classmethod
#     def get_by_name(self, name):
#         """Get the id, name, description of a role based on the role name"""
#         return self.query.filter_by(name=name).first()
