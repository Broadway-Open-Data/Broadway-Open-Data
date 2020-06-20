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

def runTime(string):
    hour, minute = string.split("hours")
    if hour == "one":
        hour = 60
    elif hour == "two":
        hour = 60 * 2
    elif hour == "three":
        hour = 60 * 3
    else:
        hour = (60 * int(hour))

    minutesWithoutIntermission = hour + int(minute.strip("minutes")
    intermission = minute.split("with")[1].strip("intermission")

    if intermission == "one":
        pass
    elif hour == "two":
        pass
    else:
        pass

    totalTime = intermission +  minutesWithoutIntermission

    return totalTime



for show_record in all_data:
    record = show_record["show_info"]
    # Delete this if it exists...
    if "table_label" in record.keys():
        del record["table_label"]

    # Add the following values:
    for x in ["show_id","year"]:
        record[x] = show_record.get(x)

    #Add Running time Key to all shows:
    if record.get("Running Time") != None:
        record[Running Time] = runTime(record.get("Running Time"))
    else:
        record[Running Time] = runTime("0 hours and 0 minutes with zero intermission")

    # Save
    all_show_info.append(record)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Save here when finished
print(f"saving data for {len(all_show_info):,} records")

save_data_path = Path(os.path.join("data","all_show_info.json"))
with open(save_data_path,"w") as f:
    json.dump(all_show_info,f)
