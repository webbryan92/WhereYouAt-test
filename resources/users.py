from flask import jsonify, Blueprint

from flask_restful import Resource, Api

import models

class UserList(Resource):
    def get(self):
        return jsonify({'users': [{'user': 'Python Basics'}]})

class User(Resource):
    def get(self, id):
        return jsonify({'user': 'Python Basics'})
    def put(self, id):
        return jsonify({'user': 'Python Basics'})
    def delete(self, id):
        return jsonify({'user': 'Python Basics'})

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)