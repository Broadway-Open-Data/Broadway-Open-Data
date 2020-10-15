"""
I'm not sure which order this will be in... But... We have a list of records of people.
Let's get data on them...
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

df.head(10)
