# Broadway Open Data
Write new documentation here.

**NOTE:** Need to explain what each of these things are doing...

## 1. Getting Started
Read the [Getting Started](https://github.com/Broadway-Open-Data/Broadway-Open-Data/blob/master/gettingStarted.md) page.

## 2. Scrape Content
*This will take > 12 hours to run...*
Mac:
```
bash scrape_content/run_web_scraper.sh
```

## 3. Structure Content
*This will take you about 1 hour:*
```
python3 structure_content/soup_to_json.py
```
*This part is very fast:*
```
python3 structure_content/get_all_show_info.py
python3 structure_content/get_all_people_info.py
```

## 4. Clean Data
```
python3 clean_data/clean_show_info.py
python3 clean_data/clean_people_info.py
```

## 5. Add to database
_You'll need login credetentials for this..._


----

## 6. Completed!
Hoorah! You're done getting all the data
