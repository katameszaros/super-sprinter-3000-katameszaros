from peewee import *
from story_manager.connect_db import ConnectDatabase

class Story(Model):
    title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = CharField()
    estimation = CharField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
