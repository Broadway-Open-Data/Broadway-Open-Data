import sys
import re
import numpy as np
import pandas as pd

def extract_date_from_opening_date(s):
    """
    input a pandas series with poorly formatted dates
    returns pandas series with datetime values
    """

    replace_dict = {
        "(Spring) ([0-9]{4})":"March 1, \\2",
        "(Fall) ([0-9]{4})": "September 1, \\2",
        "(Fall,) ([0-9]{4})": "September 1, \\2",
        # "Never officially opened":"NEVER OPENED",
        "(circa) ([0-9]{4})": "January 1, \\2",
        "(circa) (([0-9]{2}\\/){,2}[0-9]{4})": "\\2",
        "(December or November) ([0-9]{4})":"November 15, \\2",
        }

    replace_dict = {re.compile(k):v for k,v in replace_dict.items()}

    new_values = []

    for x in s.values:
        # blank values get nothing
        if not x or pd.isnull(x):
            new_values.append(None)
            continue
        # Pick up
        for k,v in replace_dict.items():
            if k.search(x):
                x = k.sub(v, x).strip()
                # new_values.append(x)
                # continue

        # If no match
        new_values.append(x)

    # convert to datetime
    # pd.Series(new_values)
    new_values = pd.to_datetime(new_values, errors="coerce", cache=True)
    return new_values


# ------------------------------------------------------------------------------

# Clean up Running Time
# Before doing this, need to investigate shows with multiple parts...
def extract_time_from_running_time(x):
    """extracts the number of minutes from the running time"""


    # These values are null
    if not x or type(x)!=str:
        return None

    # This is the case for one show... it's 2 hours...
    if x=="0200":
        return 120

    pattern_dict = {
        "one":"1",
        "two":"2",
        "three":"3",
        "four":"4",
        "five":"5",
        "hrs":"hours",
        "mins":"minutes",
        }
    pattern_dict = {re.compile(k,re.I | re.MULTILINE):v for k,v in pattern_dict.items()}

    # In the string `x` – replace any keys with the values
    for k,v in pattern_dict.items():
        if k.search(x):
            x = k.sub(v, x, 2)

    # Instantiate minutes
    total_n_minutes = 0

    # If there are hours
    n_hours = re.search("([0-9]+) hour", x.lower(), re.I)
    if n_hours:
        n_hours = n_hours.group(1)

        # convert to an int and add
        n_hours = int(n_hours)
        total_n_minutes += 60 * n_hours

    # If there are minutes
    n_minutes = re.search("([0-9]+) minutes", x, re.I)
    if n_minutes:
        n_minutes = n_minutes.group(1)

        # convert to an int and add
        total_n_minutes += int(n_minutes)

    return total_n_minutes
