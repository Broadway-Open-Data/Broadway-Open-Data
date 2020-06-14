"""
Load and clean `all_show_info.json` from the file `all_shows.json` in the folder `data/structured`
"""

# Import the usuals
import os
import re
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from IPython.display import display
sys.path.append('..')

# Set pandas display options
pd.options.display.max_rows = 20
pd.options.display.max_columns = 150
pd.options.display.width = 1500



# Load the current data
curr_data_path = Path(os.path.join("data","all_shows.json"))

with open(curr_data_path,"r") as f:
    all_data = json.load(f)

# These are the unique keys for `show_info`
show_info_keys = [
    "title",
    "Other titles",
    "table_label",
    "Opening Info",
    "Previews",
    "Opening",
    "Closing",
    "# Performances",
    "Theatres",
    "Production Type",
    "Run Type",
    "Market",
    "Running Time",
    "Intermissions",
    "Official Website",
    "Version",
    "Show type",
    "Run Type",
    ]

all_show_info = []

for show_record in all_data:
    show_info_record = show_record["show_info"]

    # Delete this if it exists...
    if "table_label" in show_info_record.keys():
        del show_info_record["table_label"]

    # Add the following values:
    for x in ["show_id","year"]:
        show_info_record[x] = show_record.get(x)

    # Save
    all_show_info.append(show_info_record)

# Save here when finished
save_data_path = Path(os.path.join("data","all_show_info.json"))
with open(save_data_path,"w") as f:
    json.dump(all_show_info,f)


# print(show_record["show_info"].keys())
