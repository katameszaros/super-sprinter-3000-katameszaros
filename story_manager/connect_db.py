from peewee import *


class ConnectDatabase:
    db = PostgresqlDatabase("user_stories")