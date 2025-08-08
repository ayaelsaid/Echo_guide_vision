# import os
import atexit
# from flask import Flask, send_from_directory
from flask import Flask
# from flask_cors import CORS
# from config import IMAGE_SAVE_DIRECTORY
from data_storage.setup_database import SetupDatabase
from data_storage.db_config import db
# from routes.home_routes import home_bp
# from routes.add_user_routes import user_bp
# from routes.start_interaction_routes import interaction_bp
# from routes.show_image import show_bp
from factory_app import create_app


"""
Main entry point for the Flask-based voice interaction system.

Responsibilities:
- Creates the Flask app using the factory pattern (`create_app`)
- Initializes the Peewee ORM database via `SetupDatabase`
- Registers Flask Blueprints for modular routing:
    - `home_bp`: Home and status routes
    - `user_bp`: User creation and management
    - `interaction_bp`: Start and manage Gemma 3n
    - `show_bp`: Serve saved images from disk
- Enables CORS globally to support cross-origin requests
- Ensures graceful shutdown by closing the Peewee database connection via `atexit`
- Runs the Flask development server on host `0.0.0.0` and port `5000`

Usage:
    python main.py

Environment:
- Uses configuration from `config.py` (e.g., `IMAGE_SAVE_DIRECTORY`)
- Assumes database setup modules are located in `data_storage/`
- Blueprints are organized under `routes/`
- App creation logic is encapsulated in `factory_app.py`

Notes:
- `use_reloader=False` prevents double initialization during development
- `debug=True` enables detailed error messages and auto-reload (except reloader disabled)
- Designed for modularity and future scalability

Endpoints:
- `/start_interaction`: Entry point for initiating voice-based interaction
- Other endpoints are registered via Blueprints

"""

# Main Program Execution
if __name__ == '__main__':
    # Initialize the Peewee ORM database setup
    database = SetupDatabase()
    database.setup_orm_database()

    app = create_app()
    print("Server ready. Use the /start_interaction endpoint to begin the interaction.")

    # Ensure the Peewee database connection is closed when the Flask app exits
    atexit.register(lambda: db.close() if not db.is_closed() else None)

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
