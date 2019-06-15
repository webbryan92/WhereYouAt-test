from flask import jsonify, Blueprint

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields)


import models
import json

class EventList(Resource):   
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
        events = [json.loads(event.to_json()) for event in models.Event.objects()]
        #TODO: append a created_at field to the api output so front-end
        #is not coupled with mongo style id's
        return {'events': events}

    def post(self):
        args = self.reqparse.parse_args()
        event = models.Event(**args)
        event.save()
        return jsonify({'events': [{'event': 'Python Basics'}]})

class Event(Resource):
    def get(self, id):
        return jsonify({'event': 'Python Basics'})
    def put(self, id):
        return jsonify({'event': 'Python Basics'})
    def delete(self, id):
        return jsonify({'event': 'Python Basics'})

events_api = Blueprint('resources.events', __name__)
api = Api(events_api)
api.add_resource(
    EventList,
    '/events',
    endpoint='events'
)
api.add_resource(
    Event,
    '/events/<int:id>',
    endpoint='event'
)