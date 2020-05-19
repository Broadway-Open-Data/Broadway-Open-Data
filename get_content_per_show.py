"""
Opens the url for each show and scrapes all raw html files, locally.
"""
import os
import re
import sys
import json
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Import custom modules
from fun.web_scraping import make_smart_request

# ------------------------------------------------------------------------------

base_url = "https://www.broadwayworld.com/"
exclude_list = ["photos", "moretodo", "multimedia"]
exclude_patten = re.compile("(" + "|".join(exclude_list) + ")\.php")


# First, make a directory for show folders
data_dir = Path("data/shows")
os.makedirs(data_dir, exist_ok=True)

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Second, load your show urls
show_urls_path = Path("data/show_url_by_year.json")
show_urls = json.loads(open(show_urls_path).read())

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Count the number of shows – Useful for chunking your loops
# (in case you don't want to overwhelm any server or your actual machine)
i = 0

# Begin looping through each one:
for key, value in show_urls.items():

    print(f"Beginning the year = {key}")
    # Make a path for that year
    year_dir = os.path.join(data_dir, key)
    os.makedirs(year_dir, exist_ok=True)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # A list of the shows for that year
    for v in value:
        # See the progress...
        if i%10==0 and i>0:
            print(f"{i=}")


        # Consider building a function which counts the number of already existing files
        # and begins i at that point – or something like that. Like the number of values
        # in a given key pair + how many directories in the "year" dir
        # ...
        # skip if not in valid range:
        if i<4450:
            i+=1
            continue

        show_id = re.search("showid=([0-9]+)", v).group(1)
        # Make a dir for that show
        show_dir = os.path.join(year_dir, "show_id_"+show_id)
        os.makedirs(show_dir, exist_ok=True)

        # Now download the cotent
        html = make_smart_request(v, temp_dir=show_dir, verify=False)
        soup = BeautifulSoup(html, features="html.parser")

        # Get links to additional internal
        all_links = soup.find_all("a", {"alt":True})
        all_links = [urljoin(base_url,x.get("href")) for x in all_links]

        #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

        # Make the request to each page, and that's all
        for url in all_links:

            # Don't include shows we don't want
            if exclude_patten.search(url):
                continue

            # Otherwise
            make_smart_request(url, temp_dir=show_dir)

            #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

            # That's all. Nothing else to do...

        i+=1 # total number of shows...

    #     # Break twice to exit
    #     if i> 1100:
    #         break
    #
    # # Break twice to exit
    # if i> 1100:
    #     break

# ------------------------------------------------------------------------------

# Once done downloading the files, can begin opening each one and extracting + structuring the data
print("Done downloading the files. You can begin opening each one and extracting + structuring the data")
