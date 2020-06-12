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
from structure_content.utils.get_page_content import get_production_info, get_creative_info, get_cast_info
# ==============================================================================

# Load the current data
def load_curr_data(data_path):
    """opens the json and returns existing data"""

    if os.path.isfile(data_path):
        with open(data_path,"r") as f:
            all_data = json.load(f)
    else:
        all_data = []

    return all_data

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -





# ------------------------------------------------------------------------------



# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def some_function(all_data):
    """Walk through my folders"""
    # Set up the path where all the data is located
    all_data_path = Path(os.path.join("data","shows"))

    all_show_ids = [x["show_id"] for x in all_data] if all_data else []

    i=0

    # Get each year
    for year in os.listdir(all_data_path):
        year_dir = os.path.join(all_data_path,year)

        # Get each show
        for show_id in os.listdir(year_dir):

            # Don't collect shows you already have
            if str_to_int(show_id, True) in all_show_ids:
                continue

            show_dir = os.path.join(year_dir,show_id)

            # Get the show id
            show_data = {
                "year":str_to_int(year),
                "show_id": str_to_int(show_id, True)
            }

            # get individual shows
            for file in os.listdir(show_dir):
                full_path = os.path.join(show_dir, file)

                # Don't load files you aren't ready to load...
                if not any([x in full_path for x in ["backstage_php", "creative_php", "cast_php"]]):
                    continue

                # Open the file & Load into a soup object
                html = open(full_path).read()
                soup = BeautifulSoup(html, features="html.parser")

                # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

                if "backstage_php" in full_path:
                    show_info = get_production_info(soup)
                    show_data.update({"show_info": show_info})

                if "creative_php" in full_path:
                    creative_info = get_creative_info(soup)
                    show_data.update({"creative_info": creative_info})

                if "cast_php" in full_path:
                    cast_info = get_cast_info(soup)
                    show_data.update({"cast_info": cast_info})



                # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


                # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


            # Save data for each show
            all_data.append(show_data)

        # Stop after a while...
        # There's a bug somewhere here -- one of the shows in this year are messed up
        if str_to_int(year)>1901:
            break


    return all_data


# ==============================================================================



if __name__ == '__main__':
    # Do this
    data_path = Path(os.path.join("data","all_show.json"))
    all_data = load_curr_data(data_path)
    n_start = len(all_data)
    all_data = some_function(all_data)
    # Save your show data
    with open(data_path,"w") as f:
        json.dump(all_data, f)

    print(f"+{len(all_data)-n_start} records ... (start with {n_start})")
