"""
Load and clean `all_show_info.json` from the file `all_shows.json` in the folder `data/structured`
"""

# Import the usuals
import os
import re
import sys
import json
import pandas as pd

from pathlib import Path
sys.path.append('..')

# Set pandas display options
pd.options.display.max_rows = 20
pd.options.display.max_columns = 150
pd.options.display.width = 1500



# Load the current data
curr_data_path = Path(os.path.join("data","all_shows_data.json"))

if not os.path.isfile(curr_data_path):
    raise AssertionError(f"file doesn't exist for '{curr_data_path}'")
    sys.exit()

with open(curr_data_path,"r") as f:
    all_data = json.load(f)

all_show_info = []

for show_record in all_data:
    record = show_record["show_info"]

    # Delete this if it exists...
    if "table_label" in record.keys():
        del record["table_label"]

    # Add the following values:
    for x in ["show_id","year"]:
        record[x] = show_record.get(x)
    # Save
    all_show_info.append(record)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Save here when finished
print(f"saving data for {len(all_show_info):,} records")

save_data_path = Path(os.path.join("data","all_show_info.json"))
with open(save_data_path,"w") as f:
    json.dump(all_show_info,f)
