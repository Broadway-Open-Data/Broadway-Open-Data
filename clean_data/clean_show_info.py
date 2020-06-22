"""
Load and clean `all_show_info.json` --> save to `all_show_info_cleaned.json`
"""

# Import the usuals
import os
import re
import sys
import json
import numpy as np
import pandas as pd
from IPython.display import display

from pathlib import Path
sys.path.append('.')

# Set pandas display options
pd.options.display.max_rows = 100
pd.options.display.max_columns = 150
pd.options.display.width = 1500

# Import custom stuff
from clean_data.utils.extract_values import extract_date_from_opening_date, extract_time_from_running_time

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Load the current data
curr_data_path = Path(os.path.join("data","all_show_info.json"))

if not os.path.isfile(curr_data_path):
    raise AssertionError(f"file doesn't exist for '{curr_data_path}'")
    sys.exit()

with open(curr_data_path,"r") as f:
    all_data = json.load(f)



# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Load to a dataframe
df = pd.DataFrame.from_records(all_data)

# Drop all columns ending with `_URL`
drop_cols = df.columns[df.columns.str.endswith("_URL")]
df.drop(columns=drop_cols, inplace=True)

# Convert relevant datetime columns
date_col = ["Opening", "Closing", "Previews"]
for col in date_col:
    df[col] = pd.to_datetime(df[col], cache=True, errors="coerce")


# ------------------------------------------------------------------------------

# Production type
production_type_dict = {"Return Engagement":"Revival", "American Premiere":"Premiere"}
df["Production Type"] = df["Production Type"].replace(production_type_dict)


# Categorical columns:
cat_cols = ["Production Type", "Run Type", "Market", "Show type", "Version", "Show type"]
for col in cat_cols:
    df[col] = df[col].astype("category")


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Numeric cols
num_cols = ["show_id","year"]
for col in num_cols:
    df[col] = df[col].astype(int)


# ------------------------------------------------------------------------------

# Clean up title
pattern = re.compile(" - Broadway .*")
df["title"] = df["title"].str.replace(pattern,"", regex=True)

# ------------------------------------------------------------------------------

# Clean up show id
df["theatre_id"] = df["theatre_id"].str.extract(r"([0-9]+$)")

# ------------------------------------------------------------------------------

# Clean up Theatres
df["Theatres"] = df["Theatres"].str.extract("(.*) \(New York")

# ------------------------------------------------------------------------------

# Simplify show type
map_dict = {
    "Play with Music":"Play",
    "Operetta":"Musical",
    "Pantomime":"Musical",
    "Solo":"Play",
    "Opera Bouffe":"Musical",
    "Vaudeville":"Musical",
    "One-Acts":"Play",
    "Ballet":"Other",
    "Dance":"Other",
    "Performance":"Other",
    "Benefit":"Other"
    }
df["Show type simple"] = df["Show type"].replace(map_dict)

# ------------------------------------------------------------------------------

# Some dates are missing...so fill them in through this column
# Extract opening date from opening info
replace_dict = {
    "unknown":None,
    "Never officially opened":None,
    "not announced":None
    }

s = extract_date_from_opening_date(df["Opening Info"])

# If use pandas method, this below gets messed up...
df["Opening"] = np.where(df["Opening"].notna(), df["Opening"], s)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


# If never opened
map_dict = {
    "unknown":None,
    "Never officially opened":True,
    "not announced":True
    }
# Also include if Opening is NA
df["Show Never Opened"] = np.where(df["Opening Info"].notna(), df["Opening Info"].map(map_dict), False)
df["Show Never Opened"] = np.where(df["Opening"].notna(), df["Show Never Opened"], True)

# Now drop that column
df.drop(columns=["Opening Info"], inplace=True)

# ------------------------------------------------------------------------------

# Clean up Intermissions
# YB: Nikil has got this...


# ------------------------------------------------------------------------------
# Clean up running time
df["Running Time"] = df["Running Time"].apply(extract_time_from_running_time)


# ------------------------------------------------------------------------------

# Revival or Original?
revival_dict = {
    'Original Production': False,
    'Revival': True,
    'Premiere': False,
    'Revised Production': False,
    'Production': False,
    'Concert': False,
    'Concert Revival': True,
    'Motion Picture': False
    }
df["Revival"] = df["Production Type"].map(revival_dict)



# ------------------------------------------------------------------------------

# Clean up Theatres
def extract_version(x):
    if not x or type(x)!=str:
        return None
    search_strings = ["pre-broadway","revival", "broadway"]
    for y in search_strings:
        if y in x.lower():
            return y
    # if nothing
    return None

# Not a meaningful column...
df["Version"] = df["Version"].apply(extract_version)


# ------------------------------------------------------------------------------

# Save here when finished
print(f"saving data for {len(df):,} records")

# save_data_path = Path(os.path.join("data","all_show_info_cleaned.json"))
# df.to_json(save_data_path, orient="records")

# Data is much smaller in CSV format...
save_data_path = Path(os.path.join("data","all_show_info_cleaned.csv"))
df.to_csv(save_data_path, index=False)
