from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse

import models

class EventList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
    def get(self):
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