"""
Parse content from existing `data/shows` folder. Store in the folder `data/structured`

investigate using this link: https://www.broadwayworld.com/shows/backstage.php?showid=313359
"""
# Import the usuals
import os
import re
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.append('.')

# Custom stuff
from utils.web_scraping import get_usable_name
from utils.string_manipulations import str_to_int
from structure_content.get_page_content import get_title, get_tables
# ==============================================================================

# Load the current data
curr_data_path = Path(os.path.join("data","all_show.json"))

if os.path.isfile(curr_data_path):
    with open(curr_data_path,"r") as f:
        all_data = json.load(f)
else:
    all_data = []

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Set up the path where all the data is located
data_path = Path(os.path.join("data","shows"))


# ------------------------------------------------------------------------------



# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def some_function():
    """Walk through my folders"""

    i=0
    all_show_data = []

    # Get each year
    for year in os.listdir(data_path):
        year_dir = os.path.join(data_path,year)

        # Get each show
        for show_id in os.listdir(year_dir):
            show_dir = os.path.join(year_dir,show_id)

            # Get the show id
            show_data = {
                "year":str_to_int(year),
                "show_id": str_to_int(show_id, True)
            }

            # get individual shows
            for file in os.listdir(show_dir):
                full_path = os.path.join(show_dir, file)

                #  NOTE: NEED TO BE STRATEGIC HERE
                #  THERE ARE MULTIPLE TYPES OF FILES
                #  EACH HAS DIFF KIND OF DATA...

                if "backstage_php" not in full_path:
                    continue

                # Open the file
                with open(full_path, "r") as f:
                    html = f.read()

                # Load into a soup object
                soup = BeautifulSoup(html, features="html.parser")

                # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

                # get title
                if "title" not in show_data.keys():
                    show_data["title"] = get_title(soup)

                all_tables = get_tables(soup)

                # Add show info
                show_data.update(all_tables.get("show_info"))

                # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


            # Save data for each show
            all_show_data.append(show_data)

        # Stop after a while...
        if int(year)>1900:
            break

    return all_show_data


# ==============================================================================



if __name__ == '__main__':
    # Do this
    show_data = some_function()
    # Save your show data
    with open(curr_data_path,"w") as f:
        json.dump(show_data, f)

    print(f"Saving data for {len(show_data)} shows.")
