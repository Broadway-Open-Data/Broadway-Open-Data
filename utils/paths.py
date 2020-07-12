import os
import sys
from pathlib import Path


def get_path_from_parents(my_path, levels=2, path_type="file"):
    """
    returns the path for a file from the parent directories.
    """

    i = 0
    while \
        (not os.path.isfile(my_path) and path_type=="file") or \
        (not os.path.isdir(my_path) and path_type=="dir"):

        my_path = Path(os.path.join("../",my_path))
        i+=1

        # Stop trying...
        if i>levels:
            raise AssertionError(f"{path_type} doesn't exist for '{my_path}'")
            sys.exit()

    # then return it
    return my_path
