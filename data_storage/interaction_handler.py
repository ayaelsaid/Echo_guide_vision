import datetime
from peewee import OperationalError
from .models import LastInteractionState, Language, Name
from .db_config import db

class GetInteraction:
    """
    Handles saving and loading the last interaction state using ORM.
    """

    def __init__(self):
        """Initializes the GetInteraction handler."""
        pass

    def save_last_interaction_orm(question, ai_response, image_path):
        """
        Saves the last interaction details.

        Args:
            question (str): User's question
            ai_response (str): AI's response
            image_path (str): Path to the image used

        Side Effects:
            - Updates LastInteractionState table (ID=1)
        """
        try:
            db.connect()
            state = LastInteractionState.get(LastInteractionState.id == 1)
            state.last_question = question
            state.last_ai_response = ai_response
            state.last_image_path = image_path
            state.timestamp = datetime.datetime.now()
            state.save()
            print("ORM: Last interaction state saved successfully.")
        except OperationalError as e:
            print(f"ORM: Database connection error during save: {e}")
        except Exception as e:
            print(f"ORM: Error saving last interaction: {e}")
        finally:
            if not db.is_closed():
                db.close()



    def load_last_interaction_orm():
        """
        Loads the last interaction details.

        Returns:
            dict: {
                "question": str,
                "ai_response": str,
                "image_path": str
            } or empty dict if not found.
        """
        db.connect()
        state_data = {}
        try:
            state = LastInteractionState.get(LastInteractionState.id == 1)
            state_data = {
                "question": state.last_question,
                "ai_response": state.last_ai_response,
                "image_path": state.last_image_path
            }
            print("ORM: Last interaction state loaded successfully.")
        except LastInteractionState.DoesNotExist:
            print("ORM: No previous interaction found (ID 1 does not exist or has no data).")
        except OperationalError as e:
            print(f"ORM: Database connection error during load: {e}")
        except Exception as e:
            print(f"ORM: Error loading last interaction: {e}")
        finally:
            if not db.is_closed():
                db.close()
        return state_data
        

