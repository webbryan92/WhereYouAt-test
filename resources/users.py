from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse, inputs

import models

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'gamertag',
            required=True,
            help='No gamertag provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'first_name',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'last_name',
            location=['form', 'json']
        )
        #TODO: handle invalid e-mails
        self.reqparse.add_argument(
            'email',
            location=['from', 'json']
        )

    def get(self):
        return jsonify({'users': [{'user': 'Python Basics'}]})

    #TODO: test post on users
    def post(self):
        args = self.reqparse.parse_args()
        user = models.User(**args)
        user.save()
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