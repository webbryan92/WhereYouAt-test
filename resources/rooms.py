from flask import jsonify, Blueprint, abort, g, make_response

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, url_for, marshal, marshal_with)
from mongoengine.errors import ValidationError
from mongoengine.queryset.visitor import Q
from auth import auth
from models import Event, User

import models
import json
import datetime


class UserField(fields.Raw):
    def format(self, obj):
        # check if property is a user object and has an id
        if isinstance(obj, User) and hasattr(obj, 'id'):
            return str(obj.id)
        return 'Error'


class EventField(fields.Raw):
    def format(self, obj):
        # check if property is a event object and has an id
        if isinstance(obj, Event) and hasattr(obj, 'id'):
            return str(obj.id)
        return 'Error'


room_fields = {
    'id': fields.String,
    'room_name': fields.String,
    'hotel': fields.String,
    'event': EventField,
    'main_venue': fields.Boolean,
    'room_number': fields.String,
    'max_occupants': fields.Integer,
    'games': fields.List(fields.String),
    'creator': UserField,
    'start_date': fields.DateTime,
    'end_date': fields.DateTime,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}


def room_or_404(room_id):
    try:
        room = models.Room.objects.get(id=room_id)
    except (models.Room.DoesNotExist, ValidationError):
        abort(404)
    else:
        return room

#TODO: attempt refactor with creator checks
# def creator_or_403(g, room_id):
#     try:
#         room = models.Room.objects(Q(creator=g.user) | Q(id=id))
#     except models.Room.DoesNotExist:
#         return make_response(json.dumps(
#                 {'error': 'That room does not exist or is not editable'}
#             ), 403)
#     else:
#         return room

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
            'creator',
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
        marshalled = [marshal(room, room_fields) for room in models.Room.objects()]
        return jsonify({'rooms': marshalled })

    @marshal_with(room_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        room = models.Room(
            creator=g.user,
            **args
            )
        room.created_at = datetime.datetime.utcnow()
        room.save()
        return (room, 201, {'Location': url_for('resources.rooms.room', id=room.id)})

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

    @marshal_with(room_fields)
    def get(self, id):
        room = room_or_404(id)
        return [json.loads(room.to_json())]

    @marshal_with(room_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            room = models.Room.objects(Q(creator=g.user) | Q(id=id))
        except models.Room.DoesNotExist:
            return make_response(json.dumps(
                {'error': 'That room does not exist or is not editable'}
            ), 403)
        room.update(**args)
        return (room, 200,
                    {'Location': url_for('resources.rooms.room', id=id)})
    
    @auth.login_required
    def delete(self, id):
        try:
            room = models.Room.objects(Q(creator=g.user) | Q(id=id))
        except models.Room.DoesNotExist:
            return make_response(json.dumps(
                {'error': 'That room does not exist or is not editable'}
            ), 403)
        room.delete()
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
