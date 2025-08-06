from peewee import *
import datetime
# from peewee import Model, IntegerField, TextField, DateTimeField
from .db_config import db

class BaseModel(Model):
    """Base model for all Peewee models to inherit from."""
    class Meta:
        database = db

class LastInteractionState(BaseModel):
    """Model to store the state of the last interaction."""
    id = IntegerField(primary_key=True, default=1)
    last_question = TextField(null=True)
    last_ai_response = TextField(null=True)
    last_image_path = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'last_interaction_state'


class Language(BaseModel):
    """Model to store the state of the last interaction."""
    id = IntegerField(primary_key=True, default=1)
    language = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'language'