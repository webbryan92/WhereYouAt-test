from flask import jsonify, Blueprint

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with)

import models

user_fields = {
    '_id': fields.Integer,
    'username': fields.String,
    'gamertag': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'access_level': fields.Integer,
    'email': fields.String,
    'created_at': fields.DateTime,
    'friend_id_list': fields.List(fields.String)
}

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
        self.reqparse.add_argument(
            'access_level',
            required=True,
            help='Access level not provided',
            location=['form', 'json'],
            type=inputs.int_range(0, 3)
        )
        self.reqparse.add_argument(
            'email',
            location=['from', 'json'],
            type= inputs.regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        )

    def get(self):
        users = models.User.objects().to_json()
        return {'users': users}

    #TODO: test post on users
    def post(self):
        #wrap mongoengine methods in try/catch for error reporting?
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