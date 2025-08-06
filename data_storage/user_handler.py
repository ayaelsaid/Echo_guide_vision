import datetime
from peewee import OperationalError
from .models import LastInteractionState, Language, Name
from .db_config import db



class GetName:
    """
    Handles saving and loading the user's name using ORM.
    """

    def __init__(self):
        """Initializes the GetName handler."""
        pass

    def save_name(name):
        """
        Saves the user's name to the database.

        Args:
            name (str): Name to save.

        Side Effects:
            - Updates Name table (ID=1)
        """
        try:
            db.connect()
            state = Name.get(Name.id == 1)
            state.name = name
            state.timestamp = datetime.datetime.now()
            state.save()
            print("ORM: Name saved successfully.")
        except OperationalError as e:
            print(f"ORM: Database connection error during save: {e}")
        except Exception as e:
            print(f"ORM: Error saving name: {e}")
        finally:
            if not db.is_closed():
                db.close()

    def load_name():
        """
        Loads the saved name from the database.

        Returns:
            dict: {"name": str} or empty dict if not found.
        """
        db.connect()
        state_data = {}
        try:
            state = Name.get(Name.id == 1)
            state_data = {
                "name": state.name,
            }
            print("ORM: Name loaded successfully.")
        except Name.DoesNotExist:
            print("ORM: No name found (ID 1 does not exist or has no data).")
        except OperationalError as e:
            print(f"ORM: Database connection error during load: {e}")
        except Exception as e:
            print(f"ORM: Error loading name: {e}")
        finally:
            if not db.is_closed():
                db.close()
        return state_data
