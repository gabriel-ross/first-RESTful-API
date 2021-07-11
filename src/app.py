import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__) # We also need to tell SQLAlchemy where to find the data.db file
# what we're saying: the SQLAlchemy database is going to live at the root folder of the project
# it doesn't *have* to be sqlite either. It can be any (SQL-based I think) database (ex. mySQL, postgreSQL, Oracle)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# This turns off the flask SQLAlchemy tracker.
# SQLAlchemy comes with one built in and disabling this frees up redundantly used resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config('PROPOGATE_EXCEPTIONS') = True
app.secret_key = 'password'
api = Api(app)

# SQLAlchemy can also create our db for us. It does this automatically, but we need to tell it 
# what tables we want it to create in it
# this decorator means the following function will run before our first request
@app.before_first_request
def create_tables():
    # this auto-creates all of tha tables we need
    # something important is that SQLAlchemy only creates tables for resources it sees which
    # comes from the imports
        # In the case of store we import Store which imports StoreModel which contains the table name and column definitions
        # Thus, if we don't have a resource for something we want to store in the database we need to import the model directly
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)













