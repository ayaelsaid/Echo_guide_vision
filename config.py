import os
# from dotenv import load_dotenv
import os

# load_dotenv()

# H_F= os.getenv("HF_KEY")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMAGE_SAVE_DIRECTORY = os.path.join(BASE_DIR, "captured_images")


DB_FILE = "echoguid_state_orm.db"

AUDIO_SAMPLERATE = 16000
AUDIO_BLOCKSIZE = 8000
AUDIO_CHANNELS = 1
AUDIO_DTYPE = 'int16'
AUDIO_RECORD_DURATION = 7
AUDIO_FOLLOW_UP_DURATION = 4

# VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# Image Storage
IMAGE_SAVE_DIRECTORY = "/captured_images"
IMAGE_FILENAME = "last_capture.jpg"

LANG_SETTINGS = {
    "ar-XA": {
        "display_name": "العربية (Standard Arabic)",
        "vosk_model_path": "model/svosk-model-ar-0.22",
        "vosk_model_zip_name": "models/vosk-model-ar-0.22.zip", 
        "vosk_model_url": "https://alphacephei.com/vosk/models/vosk-model-ar-mgb2-0.4.zip",
        "tts_voice_name": "tts_models/ar/mai/tacotron2-DDC"
    },
    "en-US": {
        "display_name": "English (US)",
        "vosk_model_path": "models/vosk-model-small-en-us-0.15",
        "vosk_model_zip_name": "models/vosk-model-small-en-us-0.15.zip",
        "vosk_model_url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "tts_voice_name": "pyttsx3"
    },
    "es-ES": {
        "display_name": "Spanish (Spain)",
        "vosk_model_path": "models/vosk-model-small-es-0.42",
        "vosk_model_zip_name": "models/vosk-model-small-es-0.42.zip",
        "vosk_model_url": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
        "tts_voice_name": "tts_models/es/css10/vits"
    },
    "fr-FR": {
        "display_name": "French (France)",
        "vosk_model_path": "models/vosk-model-small-fr-0.22",
        "vosk_model_zip_name": "models/vosk-model-small-fr-0.22.zip",
        "vosk_model_url": "https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip",
        "tts_voice_name": "tts_models/fr/css10/vits"
    },
    "de-DE": {
        "display_name": "German (Germany)",
        "vosk_model_path": "models/vosk-model-small-de-0.15",
        "vosk_model_zip_name": "models/vosk-model-small-de-0.15.zip",
        "vosk_model_url": "https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip",
        "tts_voice_name": "tts_models/de/thorsten/vits"
    }
}