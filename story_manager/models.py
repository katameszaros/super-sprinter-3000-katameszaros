from peewee import *
from story_manager.connect_db import ConnectDatabase

class Story(Model):
    title = CharField(default="")
    user_story = CharField(default="")
    acceptance_criteria = CharField(default="")
    business_value = CharField(default="")
    estimation = CharField(default="")
    status = CharField(default="")

    class Meta:
        database = ConnectDatabase.db
