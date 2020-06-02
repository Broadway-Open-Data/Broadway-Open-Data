# Broadway Open Data
_Scalable web scraping for all Broadway data (ever)._


## Getting started:

### Mac Users:
1. Create a clone of this repository: _(only do 1st time)_
```
git clone https://github.com/ybressler/Broadway-Data.git
```
2. Set current working directory to repository:
```
cd Broadway-Open-Data
```
3. create a virtual environment _(only do 1st time)_
```
python3 -m venv venv
```
4. activate the virtual environment
```
source venv/bin/activate
```
5. install requirements _(only do 1st time)_
```
pip install -r requirements.txt
```
6. run the code!
```
python3 main.py
```

### Windows Users:
1. Create a clone of this repository: _(only do 1st time)_
```
git clone https://github.com/ybressler/Broadway-Data.git
```
2. Set current working directory to repository:
```
chdir Broadway-Open-Data
```
3. create a virtual environment _(only do 1st time)_
```
python -m venv venv
```
4. activate the virtual environment
```
venv\Scripts\activate.bat
```
5. install requirements _(only do 1st time)_
```
pip install -r requirements.txt
```
6. run the code!
```
python main.py
```

----

## Making changes
When making changes, operate in a new branch (so conflicts can be reviewed and adjusted). This is accomplished by the following commands:

1. Navigate to the project directory.

**Mac:**
```
cd Documents/Broadway-Open-Data
```
**Windows:**
```
chrdir Documents\Broadway-Open-Data
```
2. List current branches:
```
git branch
```
3. Switch to the branch you want:
If the branch exists:
```
git checkout my-branch
```
If the branch doesn't exist, make a new branch and switch:
```
git checkout -b my-new-branch
```
4. Add your changes as you normally would.
```
git add .
git commit -m "this is a commit message"
```
5. When your code is ready to be merged, create a pull request from the branch tab on github's website interface.

----
