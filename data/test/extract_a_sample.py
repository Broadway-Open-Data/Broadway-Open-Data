import os
import sys
import pandas as pd

sys.path.append(".")

# import clean data:
df_shows = pd.read_csv("data/all_show_info_cleaned.csv")
df_theatres = pd.read_csv("data/all_theatre_info_cleaned.csv")

# Select all current broadway theatres
df_agg = df_shows.groupby("Theatre ID").agg({"Year":max, "Title":"count"})

# Select top theatres
top_theatres = df_agg[df_agg["Year"]>=2019]\
    .drop(columns=["Year"])\
    .sort_values("Title", ascending=False)\
    .index[:10].values



# We like this theatre
df_selected = df_shows[df_shows["Theatre ID"].isin(top_theatres)]

# Now merge with theatres
df_merged = df_selected.merge(df_theatres)

# Save to csv
df_merged.to_csv("data/test/sample_broadway_data.csv", index=False)
