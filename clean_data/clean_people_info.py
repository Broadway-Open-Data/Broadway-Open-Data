"""
Load and clean `all_people_info.json` --> save to `all_people_info_cleaned.json`
"""

# Import the usuals
import os
import re
import sys
import json
import pandas as pd
from IPython.display import display

# Custom
from nameparser import HumanName
from functools import lru_cache

from pathlib import Path
sys.path.append('..')

# Load the current data
curr_data_path = Path(os.path.join("data","all_people_info.json"))

if not os.path.isfile(curr_data_path):
    raise AssertionError(f"file doesn't exist for '{curr_data_path}'")
    sys.exit()

with open(curr_data_path,"r") as f:
    all_data = json.load(f)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Load to a dataframe
df = pd.DataFrame.from_records(all_data)

# Drop no namers
df = df[df['name']!='']

# Numeric cols
num_cols = ["show_id","year"]
for col in num_cols:
    df[col] = df[col].astype(int)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Need to convert full name to f_name, m_name, l_name

@lru_cache
def slice_full_name(name):
    return HumanName(name)



# Takes 20 seconds w/o cache
# Takes 18.4 seconds with cache
z = df['name'].apply(slice_full_name)

# zz =df['name'][z>3]


# Need to clean this up. Not sure exactly how just yet...
# I can go through and get all the people

df_names_only = df.groupby('name', as_index=False)['name_URL'].first()
df_names_only.to_csv('data/all_people_name_url_only.csv', index=False)


# Now, replace the name_URL
df_clean = df.drop(columns=['name_URL']).merge(df_names_only, on='name', how='left')
df_clean.to_csv('data/all_people_name_and_roles.csv', index=False)


# Next step --> Add the people to the db. Then --> add each person's roles... (Hopefully will associate with each show appropriately...)

df.head(10)


# ------------------------------------------------------------------------------
# Save here when finished
# print(f"saving data for {len(df):,} records")

# save_data_path = Path(os.path.join("data","all_people_info_cleaned.json"))
# df.to_json(save_data_path, orient="records")
