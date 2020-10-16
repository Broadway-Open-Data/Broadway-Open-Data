import sys
sys.path.append(".")

import numpy as np
import pandas as pd
import datetime
from functools import lru_cache

from databases import db
from databases.models import Show, Theatre, Person, Role, ShowsRolesLink
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


def add_roles(db):
    """
    Add each role
    """


    df = pd.read_csv("data/all_people_name_and_roles.csv")

    keep_cols = ['role', 'show_id', 'year', 'type', 'role_URL', 'name_URL']
    df = df[keep_cols]

    # 1.CREATE THE ROLES
    # All cast performers will be "Performer"
    all_roles = list(df[df['type']!='cast']['role'].str.lower().unique())
    all_roles.insert(0, 'performer')

    saved_roles = Role.query.with_entities(Role.name).all()
    saved_roles = [x[0] for x in saved_roles]

    for i, role_name in enumerate(all_roles):

        my_role = Role(name = role_name)

        if my_role.name in saved_roles:
            None
            # print("already exists")
        else:
            my_role.save_to_db(skip_errors=True, verbose=True)

        # Print your progress
        if i>0 and i%100==0:
            print(f"Created {i:,} of {len(all_roles):,} (%{100*i/len(all_roles):.2f})")


def add_people_and_roles(db):
    """
    Add each role and its associated person & show to the db
    """

    df = pd.read_csv("data/all_people_name_and_roles.csv")
    keep_cols = ['role', 'show_id', 'year', 'type', 'role_URL', 'name_URL']
    df = df[keep_cols]

    # Replace nan with non
    df.replace({np.nan: None}, inplace=True)

    # 2. ADD THE ROLES TO THE LINK TABLE

    # 2.1 First define some lookup functions...
    @lru_cache
    def get_person_id(name_url):
        return Person.query.filter_by(url=name_url).first().id

    @lru_cache
    def get_role_id(role_name):
        return Role.query.filter_by(name=role_name).first().id

    # 2.2 Go through each row
    for idx, row in df.iterrows():
        # What is the person's id?
        my_id = get_person_id(row['name_URL'])

        if row['type']=='cast':
            role_id = get_role_id('performer')
            extra_data=row['role']
        else:
            role_id = get_role_id(row['role'])
            extra_data = None

        my_link = ShowsRolesLink(
            person_id=my_id,
            show_id=row['show_id'],
            role_id = role_id,
            extra_data=extra_data,
            url=row['role_URL']
        )
        my_link.save_to_db(skip_errors=True, verbose=False)

        # Print your progress
        if idx>0 and idx%100==0:
            print(f"Created {idx:,} of {len(df):,} (%{100*idx/len(df):.3f})")



















# if __name__=='__main__':
#     add_shows(db)
#     add_theatres(db)
