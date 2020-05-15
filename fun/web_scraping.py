import os
import re
import requests
from urllib.parse import urlparse

# Get a usable name for the file
def get_usable_name(url, ext=".txt"):

    file_name = re.sub("[\/\.:]", "_", url) + ext
    return file_name

    # This fancy stuff below is not necessary...
    # o = urlparse(url)
    # url_domain = re.search("www\.([a-z]+)\.com", o.netloc).group(1)
    # url_path = re.search("/([a-z]+)", o.path).group(1)
    # file_name = "_".join([url_domain, url_path]) + ext

    # https://www.broadwayworld.com/browseshows.cfm?showtype=BR&open_yr=2020


def make_smart_request(url, temp_dir, verbose=False):
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
    if os.path.isfile(file_path):

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
        r = requests.get(url)
        html = r.text

        with open(file_path, "w") as f:
            f.write(html)

    # Finally
    return html
