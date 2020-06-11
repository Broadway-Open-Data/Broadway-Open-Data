import sys
import re
import json
from bs4 import BeautifulSoup

sys.path.append('..')

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

def get_production_info(soup):
    """gets all the data for the creative team"""

    data = {}
    if not type(soup) == BeautifulSoup:
        return data # Error

    # Get the title
    data["title"] = get_title(soup)

    # Get table data
    more_data = get_table(soup, table_class="production-info")
    data.update(more_data)

    return data


# ------------------------------------------------------------------------------

def get_creative_info(soup):
    """gets all the data for the production"""

    data = {}
    if not type(soup) == BeautifulSoup:
        return data # Error

    # Get table data
    more_data = get_div_table(soup, table_class="staff")
    data.update(more_data)

    return data

# ------------------------------------------------------------------------------

def get_cast_info(soup):
    """gets all the data for the cast of the show"""

    data = {}
    if not type(soup) == BeautifulSoup:
        return data # Error

    # Get table data
    more_data = get_div_table(soup, table_class="staff")
    data.update(more_data)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # This creates a list of records – will result in nested data structure
    cast = []
    table = soup.find_all("div",{"class":"info"})
    for row in table:
        row_data ={}

        # Get the values one by one
        for key in ["name","role"]:
            # first the item
            value = row.find("div",{"class":key})
            value_text = value.text
            # then its href
            value_href = value.find("a",{"href":True})
            value_href = value_href["href"] if value_href else None
            # save to row data
            row_data.update({key:value_text, key+"_URL":value_href})
        # Save each row
        cast.append(row_data)
    # At the end, add to data
    data["cast"] = cast

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    return data

# ------------------------------------------------------------------------------

def get_table(soup, table_class):
    """gets coded tables from the webpage"""

    if not type(soup) == BeautifulSoup:
        return None # Error

    # Find all tables
    tables = soup.body.find_all("table", {"class":table_class})

    data = {}

    # Which table is which?
    for tb in tables:
        table_label = tb.find_previous_sibling("h2").text
        data["table_label"] = table_label

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
            data.update(dict(tb_data))

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

        # Send them all out
        return data



# ------------------------------------------------------------------------------

def get_div_table(soup, table_class):
    """gets coded tables from the webpage"""

    if not type(soup) == BeautifulSoup:
        return None # Error

    # Find all tables
    tables = soup.body.find_all("div", {"class":table_class})

    data = {}

    # Which table is which?
    for tb in tables:
        tb_data = []

        table_label = tb.find_previous_sibling("h2").text
        data["table_label"] = table_label

        for row in tb.find_all("div"):

            row_vals = []
            # Read right to left
            for ele in row.find_all("span")[::-1]:

                # get the text
                ele_text = remove_special_chars(ele.text.strip())

                # Save your links
                if ele.find("a"):
                    href = ele.find("a",{"href":True})["href"]
                    tb_data.append([ele_text+"_URL",href])

                # Save the values from the row
                row_vals.append(ele_text)

            # Save the row value
            tb_data.append(row_vals)


        # Convert to a dict and save
        tb_data_dict = dict(tb_data)
        # Remove any blank keys
        tb_data_dict.pop('', None)
        # Update
        data.update(tb_data_dict)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 

    return data


# [<div>
# <span class="left"><a href="/people/Woody-Allen/"><strong>Woody Allen</strong></a> </span>
# <span class="right"><strong>Bookwriter</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Herbert-Farjeon/"><strong>Herbert Farjeon</strong></a> </span>
# <span class="right"><strong>Bookwriter</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Nina-Warner-Hook/"><strong>Nina Warner Hook</strong></a> </span>
# <span class="right"><strong>Bookwriter</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Jonathan-Tunick-/"><strong>Jonathan Tunick</strong></a>
# </span>
# <span class="right"><strong>Orchestrator</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Edwin-Aldridge/"><strong>Edwin Aldridge</strong></a>
# </span>
# <span class="right"><strong>Assistant Stage Manager</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Jay-Brower/"><strong>Jay Brower</strong></a>
# </span>
# <span class="right"><strong>Orchestrator</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Serge-Casal/"><strong>Serge Casal</strong></a>
# </span>
# <span class="right"><strong>Hair Designer</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Irvin-Dorfman/"><strong>Irvin Dorfman</strong></a>
# </span>
# <span class="right"><strong>General Press Representative</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Al-Goldin/"><strong>Al Goldin</strong></a>
# </span>
# <span class="right"><strong>General Manager</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Milton-Greene/"><strong>Milton Greene</strong></a>
# </span>
# <span class="right"><strong>Vocal Music Arranger</strong>
# </span>
# </div>, <div class="no-dots">
# <span class="left">
# </span>
# <span class="right"><strong>Musical Director</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Tom-Hansen/"><strong>Tom Hansen</strong></a>
# </span>
# <span class="right"><strong>Associate Director</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Ray-Harrison/"><strong>Ray Harrison</strong></a>
# </span>
# <span class="right"><strong>Choreographer</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Fred-Hearn/"><strong>Fred Hearn</strong></a>
# </span>
# <span class="right"><strong>Production Stage Manager</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Christopher-Hewett/"><strong>Christopher Hewett</strong></a>
# </span>
# <span class="right"><strong>Director</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Jack-Holmes/"><strong>Jack Holmes</strong></a>
# </span>
# <span class="right"><strong>Dance Music Arranger</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Harris-Masterson/"><strong>Harris Masterson</strong></a>
# </span>
# <span class="right"><strong>Producer</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Carroll-Masterson/"><strong>Carroll Masterson</strong></a>
# </span>
# <span class="right"><strong>Producer</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Irl-Mowery/"><strong>Irl Mowery</strong></a>
# </span>
# <span class="right"><strong>Assistant to the Producer</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Joseph-Olney/"><strong>Joseph Olney</strong></a>
# </span>
# <span class="right"><strong>Stage Manager</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/The-Shubert-Organization/"><strong>The Shubert Organization</strong></a>
# </span>
# <span class="right"><strong>Theatre Owner / Operator</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Jane-Randall/"><strong>Jane Randall</strong></a>
# </span>
# <span class="right"><strong>Press Representative</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Morris-Stonzek/"><strong>Morris Stonzek</strong></a>
# </span>
# <span class="right"><strong>Music Contractor</strong>
# </span>
# </div>, <div>
# <span class="left"><a href="/people/Fred-Voelpel/"><strong>Fred Voelpel</strong></a>
# </span>
# <span class="right"><strong>Scenic Designer</strong>
# </span>
# </div>, <div class="no-dots">
# <span class="left">
# </span>
# <span class="right"><strong>Costume Designer</strong>
# </span>
# </div>, <div class="no-dots">
# <span class="left">
# </span>
# <span class="right"><strong>Lighting Designer</strong>
# </span>
# </div>]


#
