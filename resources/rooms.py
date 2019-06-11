from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse

import models

class RoomList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
    def get(self):
        return jsonify({'rooms': [{'room': 'Python Basics'}]})

class Room(Resource):
    def get(self, id):
        return jsonify({'room': 'Python Basics'})
    def put(self, id):
        return jsonify({'room': 'Python Basics'})
    def delete(self, id):
        return jsonify({'room': 'Python Basics'})

rooms_api = Blueprint('resources.rooms', __name__)
api = Api(rooms_api)
api.add_resource(
    RoomList,
    '/rooms',
    endpoint='rooms'
)
api.add_resource(
    Room,
    '/rooms/<int:id>',
    endpoint='room'
)