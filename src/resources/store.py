from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {f'message':'store with name {name} already exists'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'unable to create store'}, 500 # 500 is internal server error - it is our fault and we don't know what it is
        return store.json(), 201


    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message':'store deleted'}, 200
        # this is unncessary as if a user is deleting the store they don't care if it didn't exist in the first
        return {'message':'store not found'}, 404

class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}, 200

        # alternately
        return {'stores':list(map(lambda x: store.json(), StoreModel.query.all()))}