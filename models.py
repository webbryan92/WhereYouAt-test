import datetime
import mongoengine as me
import mongoengine_goodjson as gj
from mongoengine.queryset.visitor import Q

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import config


me.connect('whereYouAt_test')
HASHER = PasswordHasher()

# class that will allow lookup for who modified an event
# class ModifiedBy(EmbeddedDocument):
#     user = me.ObjectIdField()
#     date = me.DateTimeFIeld

class User(gj.Document):
    username = me.StringField(required=True)
    password = me.StringField(required=True)
    display_name = me.StringField(required=True)
    first_name = me.StringField(max_length=50)
    last_name = me.StringField(max_length=50)
    access_level = me.IntField(max_value=3)
    email = me.EmailField(required=True)
    friend_id_list = me.ListField(me.StringField())
    created_at = me.DateTimeField()
    updated_at = me.DateTimeField()

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            #check if email or username exists, case insensitive
            cls.objects(Q(email=email) | Q(username__iexact=username))
        except cls.DoesNotExist:
            user = cls(username=username, email=email, **kwargs)
            user.password = user.hash_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that name or email already exists")

    
    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.objects(id=data['id'])
            return user
    
    #create a password hasher and verifier
    @staticmethod
    def hash_password(password):
        return HASHER.hash(password)

    #returns boolean
    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=3600):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


class Event(gj.Document):
    event_name = me.StringField(required=True)
    hotels = me.ListField(me.StringField(max_length=50))
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    created_at = me.DateTimeField()
    updated_at = me.DateTimeField()


class Room(gj.Document):
    room_name = me.StringField(required=True)
    hotel = me.StringField(required=True)
    main_venue = me.BooleanField(default=False)
    room_number = me.StringField(required=True)
    max_occupants = me.IntField(required=True)
    games = me.ListField(me.StringField(max_length=50))
    creator = me.ReferenceField(User)
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    event_id = me.ReferenceField(Event)
    created_at = me.DateTimeField()
    updated_at = me.DateTimeField()
