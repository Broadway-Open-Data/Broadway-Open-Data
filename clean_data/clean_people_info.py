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

# Numeric cols
num_cols = ["show_id","year"]
for col in num_cols:
    df[col] = df[col].astype(int)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Need to clean this up. Not sure exactly how just yet...


# ------------------------------------------------------------------------------
# Save here when finished
# print(f"saving data for {len(df):,} records")

# save_data_path = Path(os.path.join("data","all_people_info_cleaned.json"))
# df.to_json(save_data_path, orient="records")
