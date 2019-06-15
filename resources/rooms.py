from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse

import models

class RoomList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'room_name',
            required=True,
            help='No room name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'hotel',
            required=True,
            help='No hotel name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'main_venue',
            location=['form', 'json'],
            type=bool
        )
        self.reqparse.add_argument(
            'room_number',
            required=True,
            help='No room number provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'max_occupants',
            help='Occupants must be a number',
            location=['form', 'json'],
            type=int
        )
        self.reqparse.add_argument(
            'games',
            location=['form', 'json'],
            action='append'
        )
        self.reqparse.add_argument(
            'creator_id',
            required=True,
            help='No host user provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'start_date',
            required=True,
            help='No start date provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'end_date',
            required=True,
            help='No end date provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'event_id',
            required=True,
            help='No event id provided',
            location=['form', 'json']
        )
    def get(self):
        rooms = [json.loads(room.to_json()) for room in models.Room.objects()]
        #TODO: append a created_at field to the api output so front-end
        #is not coupled with mongo style id's
        return jsonify({'rooms': rooms })

    def post(self):
        args = self.reqparse.parse_args()
        room = models.Room(**args)
        room.save()

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