from peewee import *
import datetime
from .db_config import db

class BaseModel(Model):
    """
    Base model for all Peewee ORM models.

    Sets the shared database connection for all models via `Meta.database`.
    """
    class Meta:
        database = db

class LastInteractionState(BaseModel):
    """
    Stores the last interaction between the user and the system.

    Fields:
        - id (int): Primary key, always set to 1
        - last_question (str): The last question asked by the user
        - last_ai_response (str): The AI's response to the last question
        - last_image_path (str): Path to the image used in the interaction
        - timestamp (datetime): When the interaction was saved

    Table Name:
        'last_interaction_state'
    """
    id = IntegerField(primary_key=True, default=1)
    last_question = TextField(null=True)
    last_ai_response = TextField(null=True)
    last_image_path = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'last_interaction_state'

class Language(BaseModel):
    """
    Stores the user's selected language for interaction.

    Fields:
        - id (int): Primary key, always set to 1
        - language (str): Language code or name
        - timestamp (datetime): When the language was saved

    Table Name:
        'language'
    """
    id = IntegerField(primary_key=True, default=1)
    language = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'language'

class Name(BaseModel):
    """
    Stores the user's name for personalized interaction.

    Fields:
        - id (int): Primary key, always set to 1
        - name (str): User's name
        - timestamp (datetime): When the name was saved

    Table Name:
        'name'
    """
    id = IntegerField(primary_key=True, default=1)
    name = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'name'