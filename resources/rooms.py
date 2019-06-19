from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, inputs, fields, url_for
from mongoengine.errors import ValidationError

import models
import json
import datetime

def room_or_404(room_id):
    try:
        room = models.Room.objects.get(id = room_id)
    except (models.Room.DoesNotExist, ValidationError):
        abort(404)
    else:
        return room

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
            location=['form', 'json'],
            type=inputs.datetime_from_iso8601
        )
        self.reqparse.add_argument(
            'end_date',
            required=True,
            help='No end date provided',
            location=['form', 'json'],
            type=inputs.datetime_from_iso8601
        )
        self.reqparse.add_argument(
            'event_id',
            required=True,
            help='No event id provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        rooms = [json.loads(room.to_json()) for room in models.Room.objects()]
        return jsonify({'rooms': rooms })

    def post(self):
        args = self.reqparse.parse_args()
        room = models.Room(**args)
        room.created_at = datetime.datetime.utcnow()
        room.save()
        return "POST request successful"

class Room(Resource):
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
        super().__init__()

    def get(self, id):
        room = room_or_404(id)
        return [json.loads(room.to_json())]

    def put(self, id):
        args = self.reqparse.parse_args()
        query = room_or_404(id)
        query.update(**args)
        return ([json.loads(models.Room.objects.get(id = id).to_json())], 200,
                    {'Location': url_for('resources.rooms.room', id=id)})
    def delete(self, id):
        query = room_or_404(id)
        query.delete()
        return ('Successfully Deleted', 204, {'Location': url_for('resources.rooms.rooms')})

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