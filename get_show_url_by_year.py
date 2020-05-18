"""
Scrapes broadwayworld for urls for each show per year. Saves data locally.
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

# First, make a directory for temp files
temp_dir = Path("data/temp")
os.makedirs(temp_dir, exist_ok=True)

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Second, check if file already exists:
all_urls_dict_path = Path("data/show_url_by_year.json")
if os.path.isfile(all_urls_dict_path):
    sys.exit(f"file already exists:\n * {all_urls_dict_path=}")

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# get the starting url (links to all shows, by year)
start_url = "https://www.broadwayworld.com/browseshows.cfm?showtype=BR"
base_url = "https://www.broadwayworld.com"

# Use a function to simplify your life
html = make_smart_request(start_url, temp_dir, verbose=True)
soup = BeautifulSoup(html, features="html.parser")

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# filter for proper links
all_links = soup.body.find_all("a", href = re.compile(r'.*open_yr=[0-9]{4}'))
all_links_year = [urljoin(base_url,x.get("href")) for x in all_links]

# ------------------------------------------------------------------------------
# Loop through each year and get urls
# ------------------------------------------------------------------------------

# Make a new temp dir for year data
temp_dir = Path("data/temp/year")
os.makedirs(temp_dir, exist_ok=True)

# instantiate an empty dict
all_urls_dict = {}

# Some years have no data:
bad_years = []

for i, url in enumerate(all_links_year):
    if i%(len(all_links_year)//10)==0 and i>0:
        print(f"{i}/{len(all_links_year)}")

    year = int(re.search("([0-9]{4})", url).group())
    html = make_smart_request(url, temp_dir, verbose=False)
    soup = BeautifulSoup(html, features="html.parser") # overwrite your soup with a new soup!

    # find all urls per year
    all_links = soup.body.find_all("a", href = re.compile(r'.*showid=[0-9]+'))
    all_links_shows = [urljoin(base_url,x.get("href")) for x in all_links]

    if len(all_links_shows)==0:
        bad_years.append(year)

    # Add to dictionary
    all_urls_dict[year] = all_links_shows

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Save your url dict:
with open(all_urls_dict_path, "w") as f:
    json.dump(all_urls_dict, f)

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
