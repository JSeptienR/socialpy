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

    def get_posts(self):
        return Post.select().where(POST.user == self)

    def get_stream(self):
        pass

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(username=username, email=email, password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError('User already exists')


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        rrelated_name='posts'
    )
    content = TextField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
