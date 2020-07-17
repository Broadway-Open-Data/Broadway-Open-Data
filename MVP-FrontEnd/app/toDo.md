## UI Flask APP:
* Use flask-sqlalchemy
* Point a model to a db
 * recreate the fields (or columns) you want to access
* Create the __tablename__ and column names?
* **Create the filter using:**
 * session.query(Model).filter()
* Create an account
  * Make an API key
  * User Account with Flask (Flask-Security)
  * Manage API keys
  * Create User Table – Store User
* RESTful api endpoints

## API for Getting Data:
* No personal user account for the db necessary
* Make authenticated requests with the API key
* Create API – send json to endpoint
 * Could be a lambda
* Send a json
* Parse the json

## Visualization Tool (Shiny UI)
* plotly dash
* In the case of multiple queries:
 * Make multiple queries
 * Will be that fast...
 * Store on the client vs. server
