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
    # Test Cases
    if string == "TBA":
        return "No Running Time Info"
    elif string == "0200":
        return "120 minutes"

    timeList = string.split("hour")

    if len(timeList) == 2:  # Initial string contain 'hour'
        hour = timeList[0]
        minute = timeList[1].split("and")[1].strip("minutes")
        intermission = timeList[1].split("with")[1].strip("intermission")
        print(minute, "minute")
        print(timeList[1].split("and"), "split")
        print(timeList[1].split("and")[1], "split-index")
    elif len(timeList) == 1: # Initial string doesn't contain 'hour'
        minute = timeList.split("minutes")[0]
        intermission = timeList.split("with")[1].strip("intermission")

    if hour != None:
        if hour == "one":
            hour = 60
        elif hour == "two":
            hour = 60 * 2
        elif hour == "three":
            hour = 60 * 3
        else:
            hour = (60 * int(hour))

    minutesWithoutIntermission = int(hour or "0") + int(minute)

    if intermission == "one":
        intermission = 15
    elif hour == "two":
        intermission = 30
    else:
        intermission = 0

    totalTime = intermission +  minutesWithoutIntermission

    return "{} minutes".format(totalTime)



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
        record["Running Time"] =runTime(record.get("Running Time"))
    else:
        record["Running Time"] = "No Running Time Info"

    # Save
    all_show_info.append(record)

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Save here when finished
print(f"saving data for {len(all_show_info):,} records")

save_data_path = Path(os.path.join("data","all_show_info.json"))
with open(save_data_path,"w") as f:
    json.dump(all_show_info,f)
