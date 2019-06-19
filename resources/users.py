from flask import jsonify, Blueprint

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with)

import models
import json
import datetime

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
        users = [json.loads(user.to_json()) for user in models.User.objects()]
        return {'users': users}

    #TODO: test post on users
    def post(self):
        #wrap mongoengine methods in try/catch for error reporting?
        args = self.reqparse.parse_args()
        user = models.User(**args)
        user.created_at = datetime.datetime.utcnow()
        user.save()
        return "POST request sucessful"

class User(Resource):
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
        super().__init__()

    def get(self, id):
        user = models.User.objects.get(id = id)
        return [json.loads(user.to_json())]
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.objects.get(id = id)
        query.update(**args)
        return [json.loads(models.User.objects.get(id = id).to_json())]
    def delete(self, id):
        #TODO: delete method
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