from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, url_for, marshal, marshal_with)
from mongoengine.errors import ValidationError
from auth import auth

import models
import json
import datetime

user_fields = {
    'display_name': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

def user_or_404(user_id):
    try:
        user = models.User.objects.get(id = user_id)
    except (models.User.DoesNotExist, ValidationError): 
        abort(404)
    else:
        return user

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
        self.reqparse.add_argument(
            'password',
            required=True,
            help = 'No password verification provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help = 'No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        marshalled = [marshal(user, user_fields) for user in models.User.objects()]
        return {'users': marshalled}

    #TODO: test post on users
    @auth.login_required
    def post(self):
        #wrap mongoengine methods in try/catch for error reporting?
        args = self.reqparse.parse_args()
        # user = models.User(**args)
        # user.created_at = datetime.datetime.utcnow()
        # user.save()
        # return (user, 201, {'Location': url_for('resources.users.user', id=user.id)})
        if args.get('password') == args.get('verify_password'):
            user = models.User.create_user(**args)
            return marshal(user, user_fields), 201
        return make_response(json.dumps({
            'error': 'Passwords do not match'
            }), 400)

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

    @marshal_with(user_fields)
    @auth.login_required
    def get(self, id):
        user = models.User.objects.get(id = id)
        return [json.loads(user.to_json())]

    @marshal_with(user_fields)
    #need access levels
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        query = user_or_404(id)
        query.update(**args)
        return (query, 200,
                    {'Location': url_for('resources.users.user', id=id)})
    #need access levels
    @auth.login_required
    def delete(self, id):
        query = user_or_404(id)
        query.delete()
        return ('Successfully Deleted', 204, {'Location': url_for('resources.users.users')})

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