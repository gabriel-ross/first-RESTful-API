from db import db

'''
This user class is essentially a helper class rather than a resource. 
It isn't a resource as the API can't send or recieve data from it. 
'''
'''
A model is our internal representation of an entity - essentially an object.

A resource is the external representation - an abstraction layer to the object - 
details ways in which the object can be interacted with via external clients (like websites).
'''

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) # int arg is limit to size of username
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Can have other fields in the object, but since we didn't tell alchemy that it is a field it won't be a 
        # column in the database
        self.other_property = None

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        