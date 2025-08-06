import datetime
from peewee import OperationalError
from .models import LastInteractionState, Language, Name
from .db_config import db

class SetupDatabase:
    """
    Initializes and prepares the ORM database.

    Responsibilities:
    - Connects to the database
    - Creates required tables if they don't exist
    - Inserts default rows with ID=1 for each model
    """

    def __init__(self, database_utility):
        """
        Args:
            database_utility: Optional utility for database operations (not used here).
        """
        self.database_utility = database_utility

    def setup_orm_database():
        """
        Creates tables and inserts default records if missing.

        Side Effects:
            - Connects to the database
            - Creates tables: LastInteractionState, Language, Name
            - Inserts default row with ID=1 for each table
        """
        try:
            db.connect()
            db.create_tables([LastInteractionState, Language, Name])

            try:
                LastInteractionState.get(LastInteractionState.id == 1)
            except LastInteractionState.DoesNotExist:
                LastInteractionState.create(id=1, last_question=None, last_ai_response=None, last_image_path=None)
            try:
                Language.get(Language.id == 1)
            except Language.DoesNotExist:
                Language.create(id=1, language=None)
            print(f"ORM Database and models initialized successfully.")
            try:
                Name.get(Name.id == 1)
            except Name.DoesNotExist:
                Name.create(id=1, name=None)
            print(f"ORM Database and models initialized successfully.")

        except OperationalError as e:
            print(f"ORM: Database connection error during setup: {e}")
        except Exception as e:
            print(f"ORM: An unexpected error occurred during setup: {e}")
        finally:
            if not db.is_closed():
                db.close()


# class SetupDatabase:
#     def __init__(self, database_utility):
#         self.database_utility = database_utility
#         pass
#     def setup_orm_database():
#         """Initializes the ORM database and creates tables if they don't exist."""
        # try:
        #     db.connect()
        #     db.create_tables([LastInteractionState, Language, Name])

        #     try:
        #         LastInteractionState.get(LastInteractionState.id == 1)
        #     except LastInteractionState.DoesNotExist:
        #         LastInteractionState.create(id=1, last_question=None, last_ai_response=None, last_image_path=None)
        #     try:
        #         Language.get(Language.id == 1)
        #     except Language.DoesNotExist:
        #         Language.create(id=1, language=None)
        #     print(f"ORM Database and models initialized successfully.")
        #     try:
        #         Name.get(Name.id == 1)
        #     except Name.DoesNotExist:
        #         Name.create(id=1, name=None)
        #     print(f"ORM Database and models initialized successfully.")

        # except OperationalError as e:
        #     print(f"ORM: Database connection error during setup: {e}")
        # except Exception as e:
        #     print(f"ORM: An unexpected error occurred during setup: {e}")
        # finally:
        #     if not db.is_closed():
        #         db.close()

# class GetLanguage:
#     def __init__(self):
#         pass
#     def save_language(language):
#         """Saves the last interaction details using Peewee ORM."""
#         try:
#             db.connect()
#             state = Language.get(Language.id == 1)
#             state.language = language
#             state.timestamp = datetime.datetime.now()
#             state.save()
#             print("ORM: language saved successfully.")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during save: {e}")
#         except Exception as e:
#             print(f"ORM: Error saving language: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()

#     def load_language():
#         """Loads the last interaction details using Peewee ORM."""
#         db.connect()
#         state_data = {}
#         try:
#             state = Language.get(Language.id == 1)
#             state_data = {
#                 "language": state.language,
#             }
#             print("ORM: language loaded successfully.")
#         except Language.DoesNotExist:
#             print("ORM: No language found (ID 1 does not exist or has no data).")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during load: {e}")
#         except Exception as e:
#             print(f"ORM: Error loading language: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()
#         return state_data

# class GetName:
#     def __init__(self):
#         pass
#     def save_name(name):
#         """Saves the last interaction details using Peewee ORM."""
#         try:
#             db.connect()
#             state = Name.get(Name.id == 1)
#             state.name = name
#             state.timestamp = datetime.datetime.now()
#             state.save()
#             print("ORM: Name saved successfully.")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during save: {e}")
#         except Exception as e:
#             print(f"ORM: Error saving name: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()

#     def load_name():
#         """Loads the last interaction details using Peewee ORM."""
#         db.connect()
#         state_data = {}
#         try:
#             state = Name.get(Name.id == 1)
#             state_data = {
#                 "name": state.name,
#             }
#             print("ORM: Name loaded successfully.")
#         except Name.DoesNotExist:
#             print("ORM: No name found (ID 1 does not exist or has no data).")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during load: {e}")
#         except Exception as e:
#             print(f"ORM: Error loading name: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()
#         return state_data
# class GetInteraction:
#     def __init__(self):
#         pass
#     def save_last_interaction_orm(question, ai_response, image_path):
#         """Saves the last interaction details using Peewee ORM."""
#         try:
#             db.connect()
#             state = LastInteractionState.get(LastInteractionState.id == 1)
#             state.last_question = question
#             state.last_ai_response = ai_response
#             state.last_image_path = image_path
#             state.timestamp = datetime.datetime.now()
#             state.save()
#             print("ORM: Last interaction state saved successfully.")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during save: {e}")
#         except Exception as e:
#             print(f"ORM: Error saving last interaction: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()

#     def load_last_interaction_orm():
#         """Loads the last interaction details using Peewee ORM."""
#         db.connect()
#         state_data = {}
#         try:
#             state = LastInteractionState.get(LastInteractionState.id == 1)
#             state_data = {
#                 "question": state.last_question,
#                 "ai_response": state.last_ai_response,
#                 "image_path": state.last_image_path
#             }
#             print("ORM: Last interaction state loaded successfully.")
#         except LastInteractionState.DoesNotExist:
#             print("ORM: No previous interaction found (ID 1 does not exist or has no data).")
#         except OperationalError as e:
#             print(f"ORM: Database connection error during load: {e}")
#         except Exception as e:
#             print(f"ORM: Error loading last interaction: {e}")
#         finally:
#             if not db.is_closed():
#                 db.close()
#         return state_data
        

