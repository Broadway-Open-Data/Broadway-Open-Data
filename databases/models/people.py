from databases import db, models

# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.sql import expression
# import enum
# import json

# import custom stuff



# --------------------------------------------------------------------------


class Person(db.Model, models.dbTable):
    """"""
    __tablename__ = "person"
    id = db.Column(db.Integer,primary_key=True)
    # website_id = db.Column(db.String, db.ForeignKey('websites.id'))
    # text = db.Column(db.String())
    #
    # collected_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow) # This needs to be fixed...
    # votes = relationship("KeywordVote", back_populates="keyword")
    # # vote_date = relationship("KeywordVote", back_populates="vote_date")
    #
    # # keyword_metadata = db.Column(db.String)
    # in_which_tag = db.Column(db.String(), nullable=True)
    #
    # # Where was the tag found:
    # in_title = db.Column(db.Integer(), nullable=True)
    # in_description= db.Column(db.Integer(), nullable=True)
    #
    #
    # # Some nlp stuff
    # nlp_noun_chunks = db.Column(db.String(), nullable=True)
    # nlp_named_entities = db.Column(db.String(), nullable=True)
    # nlp_in_context_pos = db.Column(db.String(), nullable=True)
    # nlp_out_of_context_pos = db.Column(db.String(), nullable=True)

#     def __str__(self):
#         return json.dumps({
#             "id":self.id,
#             "website_id":self.website_id,
#             "text":self.text,
#             "collected_date": self.collected_date.strftime("%Y-%m-%d %H:%M:%s"),
#             "vote_date": self.collected_date.strftime("%Y-%m-%d %H:%M:%s"),
#             "in_which_tag":self.in_which_tag,
#             "in_title": self.in_title,
#             "in_description":self.in_description,
#             "nlp_noun_chunks":self.nlp_noun_chunks,
#             "nlp_named_entities":self.nlp_named_entities,
#             "nlp_in_context_pos":self.nlp_in_context_pos,
#         })
#
#
# class VoteEnum(enum.Enum):
#     superlike = "SUPERLIKE"
#     like = "LIKE"
#     dislike = "DISLIKE"
#     abstain =  "ABSTAIN"
#
#
#
# class KeywordVote(db.Model):
#     """"""
#     __tablename__ = "keyword_votes"
#     id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
#     keyword_id = db.Column(db.String, db.ForeignKey('keyword_suggestions.id'))
#     vote = db.Column(db.Enum(VoteEnum))
#     keyword = relationship("KeywordSuggestions", back_populates="votes")
#     vote_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#






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
