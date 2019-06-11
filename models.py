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
    start_date = DateTimeField()
    end_date = DateTimeField()
    #TODO: saves in localtime, convert to UTC?
    created_at = DateTimeField(default=datetime.datetime.now)

class Room(Document):
    room_name = StringField(required=True)
    hotel = StringField(required=True)
    main_venue = BooleanField(default=False)
    room_number = StringField()
    max_occupants = IntField()
    games = ListField(StringField(max_length=50))
    start_date = DateTimeField()
    end_date = DateTimeField()
    event_id = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
