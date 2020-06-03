# Import the usuals
import os
import json
import sys
import shutil

# Custom stuff
from utils.web_scraping import get_usable_name


i=0
for root, dirs, files in os.walk("data", topdown=True):
    for name in files:

        # Get full path
        full_path = os.path.join(root, name)

        # Get the file name and ext
        base, extension = os.path.splitext(name)

        # Do the renaming
        new_name = get_usable_name(base, ext=extension)
        new_root = root.replace("data","data2", 1)
        new_full_path = os.path.join(new_root, new_name)

        # Make new dirs if needed
        if not os.path.isdir(new_root):
            os.makedirs(new_root)

        # If file doesn't exist in new location, copy it...
        if not os.path.exists(new_full_path):
            shutil.copy(full_path, new_full_path)
        i+=1
