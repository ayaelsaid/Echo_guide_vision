import datetime
from peewee import OperationalError
from .models import Language
from .db_config import db

class GetLanguage:
    """
    Handles saving and loading the user's selected language using ORM.
    """

    def __init__(self):
        """Initializes the GetLanguage handler."""
        pass

    def save_language(language):
        """
        Saves the selected language to the database.

        Args:
            language (str): Language code or name to save.

        Side Effects:
            - Updates Language table (ID=1)
        """
        try:
            db.connect()
            state = Language.get(Language.id == 1)
            state.language = language
            state.timestamp = datetime.datetime.now()
            state.save()
            print("ORM: language saved successfully.")
        except OperationalError as e:
            print(f"ORM: Database connection error during save: {e}")
        except Exception as e:
            print(f"ORM: Error saving language: {e}")
        finally:
            if not db.is_closed():
                db.close()



    def load_language():
        """
        Loads the saved language from the database.

        Returns:
            dict: {"language": str} or empty dict if not found.
        """
        db.connect()
        state_data = {}
        try:
            state = Language.get(Language.id == 1)
            state_data = {
                "language": state.language,
            }
            print("ORM: language loaded successfully.")
        except Language.DoesNotExist:
            print("ORM: No language found (ID 1 does not exist or has no data).")
        except OperationalError as e:
            print(f"ORM: Database connection error during load: {e}")
        except Exception as e:
            print(f"ORM: Error loading language: {e}")
        finally:
            if not db.is_closed():
                db.close()
        return state_data
