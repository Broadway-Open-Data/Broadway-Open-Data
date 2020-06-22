import re


def str_to_int(string, regex=False):
    """attempts to convert to an int"""
    if regex:
        string = re.search("[0-9]+", string).group(0)
    try:
        v = int(string)
    except:
        v = string
    return v


# ------------------------------------------------------------------------------

def remove_special_chars(string):
    """remove unwanted characters"""

    # Remove entirely
    pattern = re.compile("[:]+")
    new_string = pattern.sub("", string)

    # remove newlines
    pattern2 = re.compile("[\n\t]+")
    new_string2 = pattern2.sub(" ", new_string)

    return new_string2
