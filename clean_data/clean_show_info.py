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
import matplotlib.pyplot as plt
from IPython.display import display

from pathlib import Path
sys.path.append('.')

# Import custom stuff
from clean_data.cd_utils.extract_values import extract_date_from_opening_date, extract_time_from_running_time, extract_n_intermissions

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
drop_cols = list(df.columns[df.columns.str.endswith("_URL")])
drop_cols.extend(["Market"])
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
cat_cols = ["Production Type", "Run Type", "Show type", "Version", "Show type"]
for col in cat_cols:
    if col in df.columns:
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

# Clean up Theatres (Probs discard later...)
df["Theatres"] = df["Theatres"].str.extract('(.+?) \(')
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

# THE FOLLOWING IS DONE MANUALLY

# Replace any shows with multiple parts
z = df["Running Time"].astype(str).str.contains("Part")

# Iterate through shows with multiple parts
for idx, row in df[z].iterrows():
    title = row["title"]
    if title == "Harry Potter and the Cursed Child":
        df.loc[idx, "Intermissions"] = 2
        df.loc[idx, "Run Time"] = 2*60 + 40 + 2*60 + 35
    if title == "Angels in America":
        df.loc[idx, "Intermissions"] = 4
        df.loc[idx, "Run Time"] = 3*60 + 30 + 4*60


# ------------------------------------------------------------------------------

# Clean up Intermissions

# Set to float (not int) because of nan values
# see this SO answer for more context: https://stackoverflow.com/a/21290084/10521959
df["Intermissions"] = df["Intermissions"].replace({"":np.nan}).astype(float)
df["Intermissions 2"] = df["Running Time"].apply(extract_n_intermissions)

# Take the highest value
df["Intermissions"] = df[["Intermissions","Intermissions 2"]].max(axis=1)

# Delete what you don't need
df.drop(columns=["Intermissions 2"], inplace=True)


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
df["Pre-Broadway"] = df["Version"].map({"broadway":False,"revival":False,"pre-broadway":True})

df.drop(columns=["Version"], inplace=True)

# ------------------------------------------------------------------------------

# Clean up run type
df["Limited Run"] = df["Run Type"].map({
    "Unknown":np.nan,
    "Open Run":False,
    "Limited Run":True,
    "Repertory (Limited Run)":True,
    "Repertory":False
    })

# Clean up run type
df["Repertory"] = df["Run Type"].map({
    "Unknown":np.nan,
    "Open Run":False,
    "Limited Run":False,
    "Repertory (Limited Run)":True,
    "Repertory":True
    })

df.drop(columns=["Run Type"], inplace=True)

# ------------------------------------------------------------------------------

# Rename some columns
df.columns = df.columns.str.title()
rename_dict = {
    "Theatre_Id":"Theatre ID",
    "Theatres":"Theatre Name (from Show Info)",
    "Show_Id":"Show ID",
    "Opening":"Opening Date",
    "Previews":"Previews Date",
    "Closing":"Closing Date",
    "# Performances":"N Performances",

}
df.rename(columns=rename_dict, inplace=True)

# ------------------------------------------------------------------------------
# Save here when finished
print(f"saving data for {len(df):,} records")

# Data is much smaller in CSV format...
save_data_path = Path(os.path.join("data","all_show_info_cleaned.csv"))
df.to_csv(save_data_path, index=False)
