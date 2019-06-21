from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, url_for, marshal, marshal_with)
from mongoengine.errors import ValidationError

import models
import json
import datetime

event_fields = {
    'id': fields.String,
    'event_name': fields.String,
    'hotels': fields.List(fields.String),
    'start_date': fields.String,
    'end_date': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

#Return the event object of id or 404 if none exists
def event_or_404(event_id):
    try:
        event = models.Event.objects.get(id = event_id)
    except (models.Event.DoesNotExist, ValidationError):
        abort(404)
    else:
        return event

class EventList(Resource):
    #Define expected fields when parsing a request
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'event_name',
            required=True,
            help='No event name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'hotels',
            location=['form', 'json'],
            action='append'
        )
        self.reqparse.add_argument(
            'start_date',
            required=True,
            help="No start date provided",
            location=['form', 'json'],
            type=inputs.date
        )
        self.reqparse.add_argument(
            'end_date',
            required=True,
            help="No end date provided",
            location=['form', 'json'],
            type=inputs.date
        )
        super().__init__()

    def get(self):
        #events = [json.loads(event.to_json()) for event in models.Event.objects()]
        marshalled = [marshal(event, event_fields) for event in models.Event.objects()]
        return {'events': marshalled}

    @marshal_with(event_fields)
    def post(self):
        args = self.reqparse.parse_args()
        event = models.Event(**args)
        event.created_at = datetime.datetime.utcnow()
        event.updated_at = datetime.datetime.utcnow()
        event.save()
        return (event, 201, {'Location': url_for('resources.events.event', id=event.id)})

class Event(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'event_name',
            required=True,
            help='No event name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'hotels',
            location=['form', 'json'],
            action='append'
        )
        self.reqparse.add_argument(
            'start_date',
            required=True,
            help="No start date provided",
            location=['form', 'json'],
            type=inputs.date
        )
        self.reqparse.add_argument(
            'end_date',
            required=True,
            help="No end date provided",
            location=['form', 'json'],
            type=inputs.date
        )
        super().__init__()

    @marshal_with(event_fields)
    def get(self, id):
        event = event_or_404(id)
        return [json.loads(event.to_json())]

    @marshal_with(event_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        args.update({'updated_at': datetime.datetime.utcnow()})
        query = event_or_404(id)
        query.update(**args)
        query.reload()
        return ([json.loads(query.to_json())], 200,
                    {'Location': url_for('resources.events.event', id=id)})
    def delete(self, id):
        query = event_or_404(id)
        query.delete()
        return ('Successfully Deleted', 204, {'Location': url_for('resources.events.events')})

events_api = Blueprint('resources.events', __name__)
api = Api(events_api)
api.add_resource(
    EventList,
    '/events',
    endpoint='events'
)
api.add_resource(
    Event,
    '/events/<string:id>',
    endpoint='event'
)