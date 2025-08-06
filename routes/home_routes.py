from controllers.home_controller import Home
from data_storage.user_handler import GetName
from flask import Blueprint

# Flask Blueprint for home-related routes
home_bp = Blueprint('home_bp', __name__)
"""
Blueprint: home_bp

Handles routing for the root ("/") endpoint, which serves either the home or welcome page
based on whether a user name is stored.
"""

# ORM handler to retrieve stored user name
get_name = GetName()

# Home controller that decides which page to render
home = Home(get_name)

@home_bp.route("/")
def home():
    """
    Root endpoint for the application.

    Flow:
        - Loads stored user name using ORM
        - If name exists → renders 'home.html'
        - If name is missing → renders 'welcome.html'

    Returns:
        Response: Rendered HTML template based on user presence
    """
    return home.get_home()