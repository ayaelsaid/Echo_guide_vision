from flask import jsonify, Blueprint
from audio_processing.listen import Record
from audio_processing.speaking.factory_speak import FactorySpeak
from data_storage.setup_database import SetupDatabase
from data_storage.interaction_handler import GetInteraction
from data_storage.lang_handler import GetLanguage
from data_storage.user_handler import GetName
from camera.camera import CameraHandler
from controllers.interaction_manager import InteractionManager
from utils.image_utils import save_pil_image_to_disk
from ai_integrations.gemma_3n import init_ai
from audio_processing.speech import Stt
from audio_processing.speaking.init_speaking import InitSpeaking
from audio_processing.speaking.which_spoken import WhichSpoken
from utils.play_audio import play_audio


# Initialize core components for interaction
camera_handler = CameraHandler()
database = SetupDatabase()
interaction = GetInteraction()
get_language = GetLanguage()
get_name = GetName()
stt = Stt(get_language)
record = Record()
init_speaking = InitSpeaking()
spoken = WhichSpoken(init_speaking.init_pyttsx3, init_speaking.init_tts, play_audio=play_audio)
factory_Speak = FactorySpeak(spoken.speak_english, spoken.speak_other_language, get_lang=get_language)


# Create interaction manager with all dependencies
interaction_manager = InteractionManager(
    camera_handler=camera_handler,
    factory_Speak=factory_Speak,
    record=record,
    stt=stt,
    save_image_func=save_pil_image_to_disk,
    interaction=interaction,
    get_name=get_name,
    init_ai=init_ai
)

# Flask Blueprint for interaction-related routes
interaction_bp = Blueprint('interaction_bp', __name__)
"""
Blueprint: interaction_bp

Handles the main interaction flow between the user and the system.
This includes capturing images, recording speech, querying AI, and responding via TTS.
"""

@interaction_bp.route('/start_interaction', methods=['POST'])
def start_interaction():
    """
    Starts the full interaction flow with the user.

    Flow:
        - Starts camera
        - Greets user via TTS
        - Captures image
        - Records and transcribes user's question
        - Sends image and question to AI model
        - Speaks AI response
        - Saves interaction state
        - Handles follow-up questions and choices

    Returns:
        JSON response with:
            - last_question (str): The user's final question
            - last_ai_response (str): AI's response to that question
            - last_image_path (str): Path to the image used in interaction

    Error Handling:
        - If any exception occurs, stops the camera and returns error JSON
    """
    try:
        final_state = interaction_manager.start_interaction_flow()
        return jsonify({
            "last_question": final_state.get("question", ""),
            "last_ai_response": final_state.get("ai_response", ""),
            "last_image_path": final_state.get("image_path", "")
        }), 200
    except Exception as e:
        print(f"General error during interaction: {e}")
        camera_handler.stop_camera()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
