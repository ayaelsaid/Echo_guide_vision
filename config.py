import os

"""
Configuration module for the voice interaction system.

This file centralizes all configurable parameters, paths, and constants used across the application.

Contents:
---------
📁 Paths:
    - BASE_DIR: Absolute path to the project root
    - MODELS_DIR: Directory for storing downloaded Vosk models
    - IMAGE_SAVE_DIRECTORY: Directory for saving captured images
    - IMAGE_FILENAME: Default filename for the last captured image
    - DB_FILE: SQLite database filename for Peewee ORM

🎙️ Audio Settings:
    - AUDIO_SAMPLERATE: Sample rate for recording (Hz)
    - AUDIO_BLOCKSIZE: Block size for audio chunks
    - AUDIO_CHANNELS: Number of audio channels (mono)
    - AUDIO_DTYPE: Data type for audio samples
    - AUDIO_RECORD_DURATION: Duration of initial recording (seconds)
    - AUDIO_FOLLOW_UP_DURATION: Duration of follow-up recording (seconds)

🌐 Language Settings:
    LANG_SETTINGS: Dictionary of supported languages with:
        - display_name: Human-readable name
        - vosk_model_path: Path to extracted Vosk model
        - vosk_model_zip_name: Filename of the ZIP model
        - vosk_model_url: URL to download the model
        - tts_voice_name: TTS engine identifier (Coqui or pyttsx3)

Notes:
------
- `HF_HOME` can be set externally to control Hugging Face cache location
- `.env` support is commented out but ready for future use
- All paths are relative to `BASE_DIR` unless overridden

Usage:
-------
Import any constant directly:
    from config import IMAGE_SAVE_DIRECTORY, LANG_SETTINGS
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
AUDIO_DIR = os.path.join(BASE_DIR, "audios")
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