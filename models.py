import datetime
import mongoengine as me
import mongoengine_goodjson as gj

me.connect('whereYouAt_test')

class User(gj.Document):
    username = me.StringField(required=True)
    gamertag = me.StringField(required=True)
    first_name = me.StringField(max_length=50)
    last_name = me.StringField(max_length=50)
    access_level = me.IntField(max_value=3)
    email = me.EmailField()
    friend_id_list = me.ListField(me.StringField())
    created_at = me.DateTimeField()

class Event(gj.Document):
    event_name = me.StringField(required=True)
    hotels = me.ListField(me.StringField(max_length=50))
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    created_at = me.DateTimeField()

class Room(gj.Document):
    room_name = me.StringField(required=True)
    hotel = me.StringField(required=True)
    main_venue = me.BooleanField(default=False)
    room_number = me.StringField(required=True)
    max_occupants = me.IntField(required=True)
    games = me.ListField(me.StringField(max_length=50))
    creator_id = me.StringField(required=True)
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    event_id = me.StringField(required=True)
    created_at = me.DateTimeField()
