from db import db

'''
Now we'll create an item model as well
'''
# Inheriting from model tells alchemy that these classes are things we want to save and retrieve from a database
# So 
class ItemModel(db.Model):
    __tablename__ = 'items'

    # id method will also be passed into the constructor, but does nothing as there is 
    # no id parameter.
    # This essentially means that we have a database that can return objects, rather than
    # having to find the data and return an object ourselves
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) # precisin is num of decimal places
    # foreign key defines a relationship between data in one table and data in another
    # the id of each store is a primary key, and the id in the item is the foreign key
    # as a result, in relational databases, you cannot delete an item whose primary key
    # is referenced by the foreign key of other items -> those items must either be deleted or their foreign key changed
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # in SQL this would be done with a join, but we don't have to do that because SQLAlchemy does that for us
    store = db.relationship('StoreModel')
    # This says that since we have a store_id, a store in the database must exist that matches the store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        '''
        All this method is doing is directly translating object to data and storing it in the db, which sqlalchemy can do for us.
        Instead of giving the database the data directly, we just tell sqlalchemy to store the object itself.
        Additionally, this can be used to update the database as well (essentially like a PUT request for a db) making the insert and update methods redundant.
        We could use the id to find the object and change its name or price, and then commit that and sqlalchemy will update the item properly
        '''
        # The session is the collection of objects we intend to write to the database. We can add several objects and commit
        # them all at once (like git) which is more efficient

        db.session.add(self)
        db.session.commit()
        

    @classmethod
    def find_by_name(cls, name): 
        # we've got ItemModel which is now a type of SQLAlchemy model
        # then we want to query the model, meaning we want to build a query on the database for aa ItemModel object
        # ultimately a database is just data, but it seems like SQLAlchemy allows us to interact with relational databases
        # as if they're storing objects directly - allowing us to query for objects and return objects directly
        # SQLAlchemy does all of the connecting, cursoring, iterating over rows for us
        #return ItemModel.query.filter_by(name=name).first() # query is a query builder that comes from sqlalchemy
        # This is saying "SELECT * FROM items WHERE name={name}"
        # .filter_by is ALSO a query builder -> we could do something like:
        # ItemModel.query.filter_by(name=name).filter_by(id=1)
        # but it'd be better to just do ItemModel.query.filter_by(name=name, id=1)
        # including .first changes our query to "SELECT * FROM items WHERE name={name} LIMIT 1"
        # which only returns the first instance

        # but since this method is a class method (as denoted by the decorator and cls arg) we can just do:
        return cls.query.filter_by(name=name).first()
    