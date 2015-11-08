import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('socialpy.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length = 100)
    join_date = DateTimeField(default = datetime.datetime.now)
    bio = CharField(default='')

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(username=username, email=email, password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError('User already exists')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
