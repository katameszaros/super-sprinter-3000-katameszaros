from peewee import *


class ConnectDatabase:
    db = PostgresqlDatabase("kata")