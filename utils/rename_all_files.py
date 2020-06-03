"""Running this code requires you to then reconcile the different directory names.
Get rid of the old one. Rename the new one..."""


# Import the usuals
import os
import json
import sys
import shutil

sys.path.append('.')

# Custom stuff
from utils.web_scraping import get_usable_name



def rename_all_files(my_dir="data"):
    """A placeholder function"""

    i=0
    for root, dirs, files in os.walk(my_dir, topdown=True):
        for name in files:

            # Get full path
            full_path = os.path.join(root, name)

            # Get the file name and ext
            base, extension = os.path.splitext(name)

            # Do the renaming
            new_name = get_usable_name(base, ext=extension)
            new_root = root.replace(my_dir,f"{my_dir}2", 1)
            new_full_path = os.path.join(new_root, new_name)

            # Make new dirs if needed
            if not os.path.isdir(new_root):
                os.makedirs(new_root)

            # If file doesn't exist in new location, copy it...
            if not os.path.exists(new_full_path):
                shutil.copy(full_path, new_full_path)
            i+=1

# ==============================================================================
# On execution:
# ==============================================================================

if __name__ == '__main__':
    # Do this
    rename_all_files()
