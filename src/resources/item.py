from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

'''
Resources should typically only contains methods for recieving HTTP requests.
Helper methods can be stored in the internal models (objects) the API 
acts on.

The principle is encapuslation. We can modify these models/methods without
altering how a client interacts with the API
'''

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
            # alternately: item = ItemModel(name **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201


    @jwt_required()
    def delete(self, name):
        # Now we can use the model to find the object and delete it
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            # if item doesn't exist we want to save it to the database
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        # This will either update the price if the item exists or insert a new one if it doesn't
        item.save_to_db()
        return item.json(), 201

    


class ItemList(Resource):

    def get(self):
        #ItemModel.query.all() returns list of all item OBJECTS in the db
        return {'items': [item.json() for item in ItemModel.query.all()]} # The return should remain {'items': [list of item JSONs]}
        # with could also do it with lambda funcs:

        # what this does is: map applies the function defined (lambda x: x.json()) to every item in the provided collection, and returns
        # an iterable map object
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


        # list comprehension is more pythonic, but map is more recognizable for people programming in other languages

        # map reduce & filter are v important in other languages