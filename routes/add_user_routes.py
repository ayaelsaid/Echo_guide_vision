from flask import request, Blueprint
from controllers.add_user_controller import User
from utils.download_extract import download_and_extract
from data_storage.lang_handler import GetLanguage
from data_storage.user_handler import GetName


# ORM handlers for language and name
get_language = GetLanguage()
get_name = GetName()

# User controller that handles user creation logic
user = User(get_name, download_and_extract, get_language)

# Flask Blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)
"""
Blueprint: user_bp

Handles user-related API routes, including adding a new user and setting up language preferences.
"""

@user_bp.route('/add_user', methods=['POST'])
def add_user():
    """
    API endpoint to add a new user and initialize their language settings.

    Expects JSON payload:
        {
            "name": "User's name",
            "language_code": "Selected language code"
        }

    Flow:
        - Extracts name and language code from request
        - Saves name and language using ORM
        - Downloads and extracts Vosk model for selected language
        - Redirects to home page on success

    Returns:
        - Flask redirect to 'home' route on success
        - JSON error response if language code is invalid
    """
    request_data = request.get_json()
    selected_language_code = request_data.get('language_code')
    name = request_data.get('name')
    return user.add_user(name, selected_language_code)