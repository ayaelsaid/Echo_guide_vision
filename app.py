import os
# import sys
import atexit
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for

from flask_cors import CORS
import PIL.Image
from config import DB_FILE, IMAGE_SAVE_DIRECTORY, MODELS_DIR, LANG_SETTINGS
from audio_processing.speech import speech_to_text
from audio_processing.listen import record_audio_once
from audio_processing.speak import speak

from camera.camera import CameraHandler
from data_storage.database import setup_orm_database, save_last_interaction_orm, load_last_interaction_orm, save_language, save_name, load_name
from data_storage.models import LastInteractionState
from data_storage.db_config import db # CORRECTED: Import db from db_config
from interaction_logic.interaction_manager import InteractionManager
from utils.image_utils import save_pil_image_to_disk
from utils.download_extract import download_and_extract

from ai_integrations.gemma_3n  import init_ai 

os.environ["HF_HOME"] = "D:/huggingface_cache"
# Initialize Flask App
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Configure static file serving for captured images
app.config['UPLOAD_FOLDER'] = os.path.join('static', IMAGE_SAVE_DIRECTORY)


camera_handler = CameraHandler()
interaction_manager = InteractionManager(camera_handler=camera_handler,
                                         speak_func=speak,
                                         record_audio_func=record_audio_once,
                                         speech_to_text_func=speech_to_text,
                                         save_image_func=save_pil_image_to_disk,
                                         save_interaction_func=save_last_interaction_orm,
                                         load_interaction_func=load_last_interaction_orm,
                                         load_name=load_name,
                                         init_ai=init_ai
                                    )

@app.route("/")
def home():
   user = load_name()
   name = user.get('name')
   if name:
       return render_template("index.html")
   else:
       return render_template("welcome.html")

@app.route('/add_user', methods=['POST'])
def add_user():
    global current_language_settings
    request_data = request.get_json()
    selected_language_code = request_data.get('language_code')
    name = request_data.get('name')
    save_name(name)

    
    lang_info = LANG_SETTINGS.get(selected_language_code)

    if not lang_info:
        return jsonify({"error": f"Language code '{selected_language_code}' is not supported."}), 400

    vosk_url = lang_info.get("vosk_model_url")
    vosk_model_local_path = lang_info.get("vosk_model_path")
    vosk_model_zip_name = lang_info.get("vosk_model_zip_name")

    vosk_zip_save_path = os.path.join(MODELS_DIR, vosk_model_zip_name)
    download_and_extract(vosk_url, vosk_zip_save_path, vosk_model_local_path)

    tts_voice_or_path = lang_info.get("tts_voice_name") 
    save_language(selected_language_code)
    current_language_settings = {
        "language_code": selected_language_code,
        "vosk_model_name": vosk_model_local_path,
        "tts_voice_name": tts_voice_or_path
    }
    return redirect(url_for('home'))




@app.route('/start_interaction', methods=['POST'])
def start_interaction():
    """
    Main entry point to start user interaction.
    Delegates the interaction flow to the InteractionManager.
    """
    try:
        final_state = interaction_manager.start_interaction_flow()
        return jsonify({
            "last_question": final_state.get("question", ""),
            "last_ai_response": final_state.get("ai_response", ""),
            "last_image_path": final_state.get("image_path", "") # This will be the full path, e.g., 'captured_images/last_capture.jpg'
        }), 200
    except Exception as e:
        print(f"General error during interaction: {e}")
        camera_handler.stop_camera() # Ensure camera is stopped on error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to serve captured images statically
@app.route('/' + IMAGE_SAVE_DIRECTORY + '/<path:filename>')
def serve_captured_image(filename):
    """Serve files from the captured_images directory."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

# Main Program Execution
if __name__ == '__main__':
    # Initialize the Peewee ORM database setup
    setup_orm_database()

    print("Server ready. Use the /start_interaction endpoint to begin the interaction.")

    # Ensure the Peewee database connection is closed when the Flask app exits
    atexit.register(lambda: db.close() if not db.is_closed() else None)

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)