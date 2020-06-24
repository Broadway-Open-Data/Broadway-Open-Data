from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import expression

from uuid import uuid4
import datetime
import enum
import json

db = SQLAlchemy()

class Show(db.Model):
    """"""
    __tablename__ = "shows"
    id = db.Column(db.String(40), primary_key=True, nullable=False, default=lambda: str(uuid4()),unique=True, index=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # add each field, manually
    title = db.Column(db.String(150), nullable=True)
    opening_date =  db.Column(db.DateTime, nullable=True)
    closing_date =  db.Column(db.DateTime, nullable=True)
    previews_date =  db.Column(db.DateTime, nullable=True)
    year = db.Column(db.Integer, index=True, nullable=True)

    # theatre
    theatre_id = db.Column(db.String(20), index=True, nullable=True)
    theatre_name = db.Column(db.String(40), index=False, nullable=True)

    # types
    production_type = db.Column(db.String(20), nullable=True)
    show_type = db.Column(db.String(20), nullable=True)
    show_type_simple = db.Column(db.String(20), nullable=True)

    # numerics
    intermissions = db.Column(db.Integer, nullable=True)
    n_performances = db.Column(db.Integer, nullable=True)
    run_time = db.Column(db.Integer, nullable=True)

    # booleans
    show_never_opened = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    revival = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    pre_broadway = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    limited_run = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    repertory = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    # Other stuff
    other_titles = db.Column(db.String(150), nullable=True)
    official_website = db.Column(db.String(40), nullable=True)

    def __str__(self):
        return json.dumps({
            "id":self.id,
            "date_instantiated":self.date_instantiated.strftime("%Y-%m-%d %H:%M:%s"),
        })


class Theatre(db.Model):
    """"""
    __tablename__ = "theatres"
    id = db.Column(db.String(50), primary_key=True, nullable=False, default=lambda: str(uuid4()),unique=True, index=True)
    date_instantiated = db.Column(db.DateTime,  nullable=False, default=datetime.datetime.utcnow)


    def __str__(self):
        return json.dumps({
            "id":self.id,
            "date_instantiated":self.date_instantiated.strftime("%Y-%m-%d %H:%M:%s"),
        })

# class WebsiteMetaData(db.Model):
#     """"""
#     __tablename__ = "websites_metadata"
#     id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
#     website_id = db.Column(db.String, db.ForeignKey('websites.id'))
#
#     # Meta stuff is below
#
#     # Deep meta
#     google_tag_manager = db.Column(db.String,  nullable=True)
#     google_tag_manager_from_gtag = db.Column(db.String,  nullable=True)
#     google_ads = db.Column(db.String,  nullable=True)
#     google_ads_from_gtag = db.Column(db.String,  nullable=True)
#     google_analytics_id = db.Column(db.String,  nullable=True)
#     google_analytics_enhancedEcommerce = db.Column(db.Boolean,  nullable=True)
#     google_analytics_anonymize_ip = db.Column(db.Boolean,  nullable=True)
#
#     # Track individual stuff
#     facebook_id = db.Column(db.String,  nullable=True)
#     facebook_app_id = db.Column(db.String,  nullable=True)
#     facebook_track = db.Column(db.String,  nullable=True)
#     hubspot = db.Column(db.String,  nullable=True)
#     hotjar_id = db.Column(db.String,  nullable=True)
#     weebly = db.Column(db.String,  nullable=True)
#     wix = db.Column(db.String,  nullable=True)
#     wordpress = db.Column(db.String,  nullable=True)
#     squarespace = db.Column(db.String,  nullable=True)
#
#     # Social media
#     facebook_profile = db.Column(db.String,  nullable=True)
#     twitter_profile = db.Column(db.String,  nullable=True)
#     instagram_profile = db.Column(db.String,  nullable=True)
#
#
#     def __str__(self):
#         return json.dumps({
#             "id":self.id,
#             "website_id":self.website_id,
#
#             # Deep meta
#             "google_tag_manager":self.google_tag_manager,
#             "google_tag_manager_from_gtag":self.google_tag_manager_from_gtag,
#             "google_ads":self.google_ads,
#             "google_ads_from_gtag":self.google_ads,
#             "google_analytics_id":self.google_analytics_id,
#             "google_analytics_enhancedEcommerce":self.google_analytics_enhancedEcommerce,
#             "google_analytics_anonymize_ip":self.google_analytics_anonymize_ip,
#
#             # Track individual stuff
#             "facebook_id":self.facebook_id,
#             "facebook_app_id":self.facebook_app_id,
#             "facebook_track":self.facebook_track,
#             "hubspot":self.hubspot,
#             "hotjar_id":self.hotjar_id,
#             "weebly":self.weebly,
#             "wix":self.wix,
#             "wordpress":self.wordpress,
#             "squarespace":self.squarespace,
#
#             # Social media
#             "facebook_profile":self.facebook_profile,
#             "twitter_profile":self.twitter_profile,
#             "instagram_profile":self.instagram_profile,
#         })
#
# # Extend the class
# all_og_tags = open("Databases/references/all_og_tags.txt", "r").read().split()
# all_meta_tags = open("Databases/references/all_meta_tags.txt", "r").read().split()
#
# # Do it here yo!
# for tag in all_og_tags+all_meta_tags:
#     setattr(WebsiteMetaData, tag, db.Column(db.String,  nullable=True))
#
#
# # ===================== END
# # =========================
#
# class WebsiteStructuredData(db.Model):
#     """"""
#     __tablename__ = "websites_structured_data"
#     id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
#     website_id = db.Column(db.String, db.ForeignKey('websites.id'))
#
#     s_name = db.Column(db.String,  nullable=True)
#     s_description = db.Column(db.String,  nullable=True)
#     s_telephone = db.Column(db.String,  nullable=True)
#     s_email = db.Column(db.String,  nullable=True)
#     s_logo = db.Column(db.String,  nullable=True)
#     s_image = db.Column(db.String,  nullable=True)
#     s_n_sub_organizations = db.Column(db.Integer,  default=0)
#
#     # Addresses
#     s_address = db.Column(db.String,  nullable=True)
#     s_address_locality = db.Column(db.String,  nullable=True)
#     s_address_region = db.Column(db.String,  nullable=True)
#     s_address_address = db.Column(db.String,  nullable=True)
#     s_address_postal_code = db.Column(db.String,  nullable=True)
#     s_linkedin = db.Column(db.String,  nullable=True)
#     s_facebook = db.Column(db.String,  nullable=True)
#     s_instagram = db.Column(db.String,  nullable=True)
#     s_youtube = db.Column(db.String,  nullable=True)
#     s_twitter = db.Column(db.String,  nullable=True)
#
#     def __str__(self):
#
#
#         return json.dumps({
#             "id":self.id,
#             "website_id":self.website_id,
#
#             "s_name":self.s_name,
#             "s_description":self.s_description,
#             "s_logo":self.s_logo,
#             "s_n_sub_organizations":self.s_n_sub_organizations,
#             "s_address_locality":self.s_address_locality,
#             "s_address_region":self.s_address_region,
#             "s_address_address":self.s_address_address,
#             "s_address_postal_code":self.s_address_postal_code,
#             "s_linkedin":self.s_linkedin,
#             "s_facebook":self.s_facebook,
#             "s_instagram":self.s_instagram,
#             "s_youtube":self.s_youtube,
#             "s_twitter":self.s_twitter,
#         })
#
#
# class KeywordSuggestions(db.Model):
#     """"""
#     __tablename__ = "keyword_suggestions"
#     id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()), unique=True)
#     website_id = db.Column(db.String, db.ForeignKey('websites.id'))
#     text = db.Column(db.String())
#
#     collected_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow) # This needs to be fixed...
#     votes = relationship("KeywordVote", back_populates="keyword")
#     # vote_date = relationship("KeywordVote", back_populates="vote_date")
#
#     # keyword_metadata = db.Column(db.String)
#     in_which_tag = db.Column(db.String(), nullable=True)
#
#     # Where was the tag found:
#     in_title = db.Column(db.Integer(), nullable=True)
#     in_description= db.Column(db.Integer(), nullable=True)
#
#
#     # Some nlp stuff
#     nlp_noun_chunks = db.Column(db.String(), nullable=True)
#     nlp_named_entities = db.Column(db.String(), nullable=True)
#     nlp_in_context_pos = db.Column(db.String(), nullable=True)
#     # nlp_out_of_context_pos = db.Column(db.String(), nullable=True)
#
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
#
#     def __str__(self):
#         return json.dumps({
#             "id":self.id,
#             "keyword_id":self.keyword_id,
#             "vote":self.vote.value,
#             # This works!!!
#             # Keywords do not though
#             # "keyword": self.keyword.values(),
#             "vote_date": self.vote_date.strftime("%Y-%m-%d %H:%M:%s"),
#         })
