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
