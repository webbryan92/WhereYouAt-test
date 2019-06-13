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
    #TODO: saves in localtime, convert to UTC?
    created_at = DateTimeField(default=datetime.datetime.now)
    friend_id_list = ListField(StringField())

class Event(Document):
    event_name = StringField(required=True)
    hotels = ListField(StringField(max_length=50))
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    #TODO: saves in localtime, convert to UTC?
    created_at = DateTimeField(default=datetime.datetime.now)

class Room(Document):
    room_name = StringField(required=True)
    hotel = StringField(required=True)
    main_venue = BooleanField(default=False)
    room_number = StringField(required=True)
    max_occupants = IntField(required=True)
    games = ListField(StringField(max_length=50))
    creator_id = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    event_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
