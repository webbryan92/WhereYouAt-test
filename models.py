import datetime
from mongoengine import *

connect('whereYouAt_test')

class User(Document):
    username = StringField(required=True)
    gamertag = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    access_level = IntField(max_value=3)
    email = EmailField()
    created_at = DateTimeField(default=datetime.datetime.now)
    #friend_id_list = ListField(StringField())

class Event(Document):
    eventName = StringField(required=True)
    hotels = ListField(StringField(max_length=50))
    start_date = DateTimeField()
    end_date = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)

class Room(Document):
    room_name = StringField(required=True)
    hotel = StringField(required=True)
    room_number = IntField()
    max_occupants = IntField()
    games = ListField(StringField(max_length=50))
    start_date = DateTimeField()
    end_date = DateTimeField()
    event_id = StringField()
    #boolean when the room is same as venue?
