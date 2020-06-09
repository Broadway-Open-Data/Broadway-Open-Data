
import re
import json
from bs4 import BeautifulSoup

# Custom stuff
from utils.string_manipulations import str_to_int, remove_special_chars


# ------------------------------------------------------------------------------

def get_title(soup, regex=True):
    """gets the title of the show"""

    if not type(soup) == BeautifulSoup:
        return None # Error

    # Otherwise, proceed
    title = soup.head.title.text

    # Parse for show title
    # "King Henry VIII - 1799 Broadway - Backstage & Production Info"
    if regex:
        pattern = re.compile("(.*) - [0-9]{4} Broadway")
        title = pattern.search(title).group(1) # If this breaks, will have to figure out why...

    # Finally
    return title

# ------------------------------------------------------------------------------

get_X_id = lambda x: str_to_int(re.search("theatre_id=([0-9]+)", x).group(1))

# ------------------------------------------------------------------------------

def get_tables(soup):
    """gets coded tables from the webpage"""

    if not type(soup) == BeautifulSoup:
        return None # Error

    # Find all tables
    tables = soup.body.find_all("table", {"class":True})

    all_tables = {}

    # Which table is which?
    for tb in tables:
        table_label = tb.find_previous_sibling("h2").text

        # We don't want this
        if "Other Productions" in table_label:
            continue

        # This is the one we want
        if table_label.endswith("Show Information"):

            # Initalize empty list (put data here)
            tb_data = []

            # get the table body
            tb_body = tb.find('tbody')

            # Get each row, then loop
            rows = tb_body.find_all('tr')

            for row in rows:
                row_vals = []

                # If there's a link, get the link
                for ele in row.find_all('td'):

                    if ele.find("a"):
                        href = ele.find("a",{"href":True})["href"]

                        # If you have a theatre_id, save it
                        if row_vals[0]=="Theatres:":
                            theatre_id = get_X_id(href)
                            tb_data.append(["theatre_id",theatre_id])


                    # Otherwise, continue
                    ele = remove_special_chars(ele.text.strip())

                    # Save the values from the row
                    row_vals.append(ele)

                # Save the row value
                tb_data.append(row_vals)

            # Convert to a dict and save
            all_tables["show_info"] = dict(tb_data)

        # Send them all out
        return all_tables







# ------------------------------------------------------------------------------
