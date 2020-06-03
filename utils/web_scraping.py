import os
import re
from pathlib import Path
import requests
import urllib3
from urllib.parse import urlparse

# Disable warnings
urllib3.disable_warnings()

# Get a usable name for the file
def get_usable_name(url, ext=".txt"):
    forbidden_chars = ["\/", "\.", ":","<",">","\"","\\","\|","\?","\*"]
    forbidden_chars = "".join(forbidden_chars)
    file_name = re.sub(f"[{forbidden_chars}]", "_", url) + ext
    return file_name

    # https://www.broadwayworld.com/browseshows.cfm?showtype=BR&open_yr=2020


def make_smart_request(url, temp_dir, verify=True, verbose=False):
    """
    Makes a smart request to a url. Saves response locally to `temp_dir`.
    If the request was previously made, data is loaded from local file.

    --
    params:
        url: the url which you're requesting
        temp_dir: the directory which to store the request response
    """

    # First, get a proper name for the url
    file_path = get_usable_name(url)
    file_path = os.path.join(temp_dir, file_path) # Locate in proper dir

    # Check if opened
    if os.path.isfile(Path(file_path)):

        # Option for printing
        if verbose:
            print(f"loading {url=} from local file")

        # Load the file
        with open(file_path, "r") as f:
            html = f.read()


    else:
        # Option for printing
        if verbose:
            print(f"making request from {url=}")

        # Make the request
        r = requests.get(url, verify=False, timeout=20)
        html = r.text

        with open(file_path, "w") as f:
            f.write(html)

    # Finally
    return html
