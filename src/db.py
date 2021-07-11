from flask_sqlalchemy import SQLAlchemy

# This object will look at all of our objects in our flask app
# and allow us to map them to database
# ex. if we create an item model object with name and price fields
# SQLAlchemy will allow us to map items by those properties to a table
db = SQLAlchemy()









