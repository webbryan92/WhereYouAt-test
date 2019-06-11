import datetime
from mongoengine import *

connect('whereYouAt_test')

class User(Document):
    username = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    accessType = IntField(max_value= 3)
    created_at = DateTimeField(default=datetime.datetime.now)
    #TODO: add other fields after tutorial
    #friend_id_list = ListField(StringField())

class Event(Document):
    eventName = StringField(required=True)
    hotels = ListField(StringField(max_length=50))
    startDate = DateTimeField()
    endDate = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)

