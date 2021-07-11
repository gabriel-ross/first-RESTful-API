from db import db

# we create the model first as the resource stands atop the model. the model is the 
# database inteface for a certain object & the resource essentially translates 
# HTTP requests into model methods

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # in the StoreModel now we can do a back-reference, allowing the store
    # to track all of the items whose foreign key matches the store's primary key

    # we have a relationship with ItemModel -> SQLAlchemy goes into ItemModel and sees that
    # the ItemModel has a foreign key that matches it to a store
    # this is a list of item models -> SQLAlchemy knows it is a many-one relationship
    items = db.relationship('ItemModel', lazy='dynamic') # lazy converts items from a list of all items to a query builder that lets us query items that reference this store

    # so whenever we create a store, we're going to create an ItemModel object for each item in the store
    # this can be expensive if we have a lot of items. Of course, we can tell SQLAlchemy not to do that lol

    def __init__(self, name):
        self.name = name
        self.items = []

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]} # returns list of item jsons
        # we need self.items.all() when using lazy 

        '''
        What lazy dynamic changes is that when it is off we'll pre-load the store essentially -> when we create the store we'll also load up all items associated, 
        but that means when we query its items we're just iterating over a list instead of accessing a table in a database. If we use lazy dynamic the up-front cost is lower,
        but every time we want the json representation of an item/all items it means we need to go into a table in the database
        '''

        # alternately using map 
        return {'name':self.name, 'items':list(map(lambda x: x.json(), self.items.all()))}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name): 
        return cls.query.filter_by(name=name).first()