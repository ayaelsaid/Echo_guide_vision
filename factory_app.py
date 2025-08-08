# import os
# import atexit
# from flask import Flask, send_from_directory
from flask import Flask
from flask_cors import CORS
# from config import IMAGE_SAVE_DIRECTORY
from routes.home_routes import home_bp
from routes.add_user_routes import user_bp
from routes.start_interaction_routes import interaction_bp
from routes.show_image import image_bp

os.environ["HF_HOME"] = "D:/huggingface_cache"
def create_app():
    """
    Factory function to create and configure the Flask application instance.

    Responsibilities:
    - Initializes the Flask app
    - Enables Cross-Origin Resource Sharing (CORS) for all routes
    - Registers modular Blueprints for routing:
        - `home_bp`: Home and status endpoints
        - `user_bp`: User creation and management
        - `interaction_bp`: Voice interaction logic
        - `show_bp`: Serve saved images from disk
    - Sets Hugging Face cache directory via `HF_HOME` environment variable

    Returns:
        Flask: Configured Flask application instance

    Notes:
    - Static file serving for images is handled via `show_bp`
    - Environment variable `HF_HOME` is set globally before app creation
    - Designed for modularity and clean separation of concerns
    """
 
    app = Flask(__name__)
    
    CORS(app)


    # Register routes
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(interaction_bp)
    app.register_blueprint(image_bp)

    return app
