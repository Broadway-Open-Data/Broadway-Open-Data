"""
Program collects data for all broadway theaters
"""

# Import the usuals
import os
import re
import sys
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


from pathlib import Path
sys.path.append('.')


# Import custom stuff
from utils.web_scraping import make_smart_request
from utils.string_manipulations import str_to_int, remove_special_chars
from structure_content.utils.get_page_content import get_data_from_theatre_soup
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
df["theatre_id"] = df["theatre_id"].str.extract(r"([0-9]+$)")
all_theatres = df["theatre_id"].dropna().unique()

# delete what you don't need
del df



# ------------------------------------------------------------------------------
# Now begin scraping each page
base_url = "https://www.broadwayworld.com/shows/theatre.php?theatre_id="

# Make a directory to save everything to
save_dir = Path("data/theatres")
os.makedirs(save_dir, exist_ok=True)

all_records = []
for theatre_id in all_theatres:

    theatre_url = base_url + theatre_id
    html = make_smart_request(theatre_url,save_dir, verbose=False)
    soup = BeautifulSoup(html, features="html.parser")
    record = get_data_from_theatre_soup(soup)
    record.update({"Theatre ID":theatre_id})
    all_records.append(record)


file_name = os.path.join("data", "all_theatre_info.json")
with open(file_name, "w") as f:
    json.dump(all_records,f)

# ------------------------------------------------------------------------------
# Structure the data
df = pd.DataFrame(all_records)

rename_dict = {
    "CLOSED":"Year Closed",
    "DEMOLISHED":"Year Demolished",
    "APPROX. SEATING CAPACITY":"Capacity",
    }
df.rename(columns=rename_dict,inplace=True)

for col in ["Year Closed","Year Demolished","Capacity"]:
    df[col] = df[col].astype(str).apply(lambda x: ''.join(re.findall("[0-9]+",x)))
    df[col] = df[col].replace({"":np.nan}).astype(float)

df["theatre name"] = df["theatre name"].str.extract('(.+?) Theater')

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


# Save the data
file_name = os.path.join("data", "all_theatre_info_cleaned.csv")
df.to_csv(file_name, index=False)
