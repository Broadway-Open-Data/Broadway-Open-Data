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
    return HumanName(name).as_dict()

# Takes about 3 minutes + 10 seconds...
df_name = df['name'].apply(slice_full_name).apply(pd.Series).add_prefix("name_")
df_clean = pd.concat([df, df_name], axis=1, join='inner')


# zz =df['name'][z>3]


# Need to clean this up. Not sure exactly how just yet...
# I can go through and get all the people

keep_cols = [x for x in df_clean.columns if 'name' in x]
df_names_only = df_clean.groupby('name', as_index=False).first()[keep_cols]
df_names_only.to_csv('data/all_people_name_url_only.csv', index=False)


# Clean it up – in case there are mispellings or whatever...
drop_cols = [x for x in df_clean.columns if 'name_' in x]
df_clean_2 = df_clean.drop(columns=drop_cols).merge(df_names_only, on='name', how='left')
df_clean_2.to_csv('data/all_people_name_and_roles.csv', index=False)


# ------------------------------------------------------------------------------
# Save here when finished
print(f"saving data for {len(df_clean_2):,} records")
