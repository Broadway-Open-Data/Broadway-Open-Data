"""
Load and clean `all_people_info.json` from the file `all_shows.json`
in the folder `data/structured`
"""

# Import the usuals
import os
import re
import sys
import json

import pandas as pd
pd.options.display.max_rows = 20
pd.options.display.max_columns = 150
pd.options.display.width = 1500

from pathlib import Path
sys.path.append('..')

# Load the current data
curr_data_path = Path(os.path.join("data","all_shows_data.json"))

if not os.path.isfile(curr_data_path):
    raise AssertionError(f"file doesn't exist for '{curr_data_path}'")
    sys.exit()

with open(curr_data_path,"r") as f:
    all_data = json.load(f)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

all_people_info = []

for show_record in all_data:

    # get identifying keys
    show_id = show_record["show_id"]
    year = show_record["year"]

    # --------------------------------------------------------------------------

    # First do all creative people
    record = show_record["creative_info"]

    # Delete this if it exists...
    if "table_label" in record.keys():
        del record["table_label"]

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Get the keys with urls
    url_data = {}
    for k,v in record.items():
        if k.endswith("_URL"):
            url_data[k.split("_URL")[0]] = v


    # now loop a second time
    for k,v in record.items():
        if not k.endswith("_URL"):
            rec = {
                "role":k,
                "name":v,
                "show_id":show_id,
                "year":year,
                "name_URL":url_data.get(v),
                "type":"creative"
            }
            # Save
            all_people_info.append(rec)
    # --------------------------------------------------------------------------
    # Next, do all cast
    record = show_record["cast_info"]["cast"]
    update_info = {"show_id":show_id, "year":year, "type":"cast"}
    for rec in record:
        rec.update(update_info)
        all_people_info.append(rec)
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # Done with the record
    # break

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
print(f"saving data for {len(all_people_info):,} records")

# Save here when finished
save_data_path = Path(os.path.join("data","all_people_info.json"))
with open(save_data_path,"w") as f:
    json.dump(all_people_info,f)
