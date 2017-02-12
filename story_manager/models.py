from peewee import *
from story_manager.connect_db import ConnectDatabase


class BaseModel(Model):

    class Meta:
        database = ConnectDatabase.db


class Status(BaseModel):
    PLANNING = "Planning"
    TO_DO = "To do"
    IN_PROGRESS = "In progress"
    REVIEW = "Review"
    DONE = "Done"

    status_text = CharField(default="")

    @classmethod
    def create_defaults(cls):
        Status(status_text=Status.PLANNING).save()
        Status(status_text=Status.TO_DO).save()
        Status(status_text=Status.IN_PROGRESS).save()
        Status(status_text=Status.REVIEW).save()
        Status(status_text=Status.DONE).save()


class Story(BaseModel):
    title = CharField(default="")
    user_story = CharField(default="", max_length=10000)
    acceptance_criteria = CharField(default="", max_length=10000)
    business_value = CharField(default="")
    estimation = CharField(default="")
    status = ForeignKeyField(Status)

    @classmethod
    def empty(cls):
        return Story(status=Status.select().where(Status.status_text == Status.PLANNING))
