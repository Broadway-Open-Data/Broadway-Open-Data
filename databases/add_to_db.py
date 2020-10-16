import sys
sys.path.append(".")

import numpy as np
import pandas as pd
import datetime

from databases import db
from databases.models import Show, Theatre, Person, Role
from sqlalchemy.exc import IntegrityError

pd.options.display.max_rows = 100

# ------------------------------------------------------------------------------

def add_shows(db):
    """
    Add all shows to the db
    """

    # Get all existing show id's
    query_shows = db.session.query(Show.id).all()
    all_show_ids = [int(x[0]) for x in query_shows]


    # ------------------------------------------------------------------------------
    # Now load the data for shows
    df = pd.read_csv("data/all_show_info_cleaned.csv")

    # Match up these columns with each other...
    cols_mapper = {x:x.lower().replace("-","_").replace(" ","_") for x in df.columns}

    cols_mapper.update({
        "Theatre Name (from Show Info)":"theatre_name",
        "Show ID":"id",
        "Running Time":"run_time"
    })

    bool_cols = ["Show Never Opened","Revival","Pre-Broadway","Limited Run","Repertory"]
    df[bool_cols] = df[bool_cols].fillna(False)
    df["Theatre ID"] = df["Theatre ID"].fillna(0)
    # Fill na values
    df = df.where((pd.notnull(df)), None)

    # This can be used to reference the columns in the sql schema
    # sql_cols = Show.__table__.columns.keys()

    # Do these things now.. .
    now = datetime.datetime.utcnow()

    for idx, row in df.iterrows():

        # don't add shows you already have
        if row["Show ID"] in all_show_ids:
            continue

        show_data = {v:row[k] for k,v in cols_mapper.items() }
        show_data.update({"date_instantiated":now})

        my_show = Show(**show_data)
        db.session.add(my_show)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    # delete what you don't need
    del df
    print("shows complete")


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

def add_theatres(db):
    """
    Add all theatres to the db
    """

    query_theatres = db.session.query(Theatre.id).all()
    all_theatre_ids = [int(x[0]) for x in query_theatres]

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Now load the data for theatres
    df = pd.read_csv("data/all_theatre_info_cleaned.csv")
    # set df type
    df["Theatre ID"] = df["Theatre ID"].fillna(0).astype(int)

    # fill in na
    df = df.where((pd.notnull(df)), None)
    # Match up these columns with each other...

    cols_mapper = {
        "Theatre ID":"id",
        "theatre name": "theatre_name",
        "streetAddress":"street_address",
        "addressLocality":"address_locality",
        "addressRegion":"address_region",
        "postalCode":"postal_code",
        "Year Closed":"year_closed",
        "Year Demolished":"year_demolished",
        "Capacity":"capacity"
        }

    now = datetime.datetime.utcnow()

    for idx, row in df.iterrows():


        # don't add shows you already have
        if row["Theatre ID"] in all_theatre_ids:
            continue

        # now get the data
        theatre_data = {v:row[k] for k,v in cols_mapper.items() }
        theatre_data.update({"date_instantiated":now})

        my_theatre = Theatre(**theatre_data)

        db.session.add(my_theatre)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    # delete what you don't need
    del df
    print("theatres complete")




def add_people(db):
    """
    Add all people to the db
    """


    df = pd.read_csv("data/all_people_name_only.csv")

    # We don't need the full name
    df.drop(columns=['name'], inplace=True)

    cols_mapper = {
        "name_URL": "url",
        "name_title":"name_title",
        "name_first":"f_name",
        "name_middle":"m_name",
        "name_last":"l_name",
        "name_suffix Closed":"name_suffix",
        "name_nickname":"name_nickname",
        }
    df.rename(columns=cols_mapper, inplace=True)

    # Replace nan with non
    df.replace({np.nan: None}, inplace=True)

    # Go through each row
    for idx, row in df.iterrows():

        # This can prob be sped up, but I don't care rn...
        res = Person.query.filter_by(url=row['url']).first()
        if res:
            None
            # print(f"\t data already commited for {idx=}")
        else:
            my_person = Person(**row)

            my_person.save_to_db()
        #
        if idx>0 and idx %10**3==0:
            print(f"Downloaded {idx:,} of {len(df):,} (%{100*idx/len(df):.3f})")

        # if idx>10**3:
        #     break


# ------------------------------------------------------------------------------


def add_people_and_roles(db):
    """
    Add each role and its associated person & show to the db
    """


    df = pd.read_csv("data/all_people_name_and_roles.csv")

    # We don't need the full name
    df.drop(columns=['name'], inplace=True)

    keep_cols = ['role', 'show_id', 'year', 'type', 'role_URL', 'name_URL']
    df = df[keep_cols]

    # Step 1 is to create the roles
    # All cast performers will be "Performer"
    all_roles = ['Performer']

    # for role_name in all_roles:
    #     my_role = Role(
    #         name = role_name
    #         )
    #     print(my_role)



    all_roles = df[df['type']!='cast']['role'].unique()
    with open("data/all_roles.txt", "w") as f:
        f.write("\n".join(all_roles))

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(40), unique=True, nullable=False)
    # type = db.Column(db.String(40), unique=False, nullable=True)
    # description = db.Column(db.String(255), unique=False, nullable=True)
    #

    # print(df[['role', 'role_URL']].iloc[:10])
    # cols_mapper = {
    #     "name_URL": "url",
    #     "name_title":"name_title",
    #     "name_first":"f_name",
    #     "name_middle":"m_name",
    #     "name_last":"l_name",
    #     "name_suffix Closed":"name_suffix",
    #     "name_nickname":"name_nickname",
    #     }
    # df.rename(columns=cols_mapper, inplace=True)
    #
    # # Replace nan with non
    # df.replace({np.nan: None}, inplace=True)
    #
    # # Go through each row
    # for idx, row in df.iterrows():
    #
    #     # This can prob be sped up, but I don't care rn...
    #     res = Person.query.filter_by(url=row['url']).first()
    #     if res:
    #         None
    #         # print(f"\t data already commited for {idx=}")
    #     else:
    #         my_person = Person(**row)
    #
    #         my_person.save_to_db()
    #     #
    #     if idx>0 and idx %10**3==0:
    #         print(f"Downloaded {idx:,} of {len(df):,} (%{100*idx/len(df):.3f})")

        # if idx>10**3:
        #     break















# if __name__=='__main__':
#     add_shows(db)
#     add_theatres(db)
