"""
Visualize results from structuring content.

Use with the `Hydrogen` package in Atom to see results neatly...
"""

# Import the usuals
import os
import re
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from IPython.display import display
sys.path.append('..')

# Set pandas display options
pd.options.display.max_rows = 20
pd.options.display.max_columns = 150
pd.options.display.width = 1500

# Load the current data
curr_data_path = Path(os.path.join("data","all_shows.json"))

with open(curr_data_path,"r") as f:
    all_data = json.load(f)


df = pd.json_normalize(all_data)

drop_cols = df.columns[df.columns.str.endswith('_URL')]
df.drop(columns=drop_cols, inplace=True)

# Visualize
display(df.shape)

plt.figure(figsize=(10,4))
df["year"].hist(bins=100)

plt.title("Broadway Shows / Year", weight="bold", size=14)
plt.show()

# ------------------------------------------------------------------------------
