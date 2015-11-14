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
        order_by = ('-join_date',)

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(Post.user == self)

    def following(self):
        """ The users that we are following """
        return (
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Reltionship.from_user == self
            )
        )

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
        related_name='posts'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True)
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
