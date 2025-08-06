from flask import jsonify, redirect, url_for
import os
from config import LANG_SETTINGS, MODELS_DIR

class User:
    """
    Handles user-related operations including saving user info,
    downloading language models, and setting language preferences.

    Dependencies:
        - get_name: Object with method save_name(name)
        - download_and_extract: Function to download and extract model files
        - get_language: Object with method save_language(code)
    """

    def __init__(self, get_name, download_and_extract, get_language):
        """
        Initializes the User handler with required dependencies.

        Args:
            get_name: Object responsible for saving user names.
            download_and_extract: Function to download and extract model files.
            get_language: Object responsible for saving language preferences.
        """
        self.get_name = get_name
        self.download_and_extract = download_and_extract
        self.get_language = get_language

    def add_user(self, name, selected_language_code):
        """
        Adds a new user, sets their language preferences, and downloads required models.

        Args:
            name (str): The name of the user.
            selected_language_code (str): Language code selected by the user.

        Returns:
            Response: Flask redirect to 'home' route on success,
                      or JSON error response if language code is invalid.

        Side Effects:
            - Saves user name and language preference.
            - Downloads and extracts Vosk model for selected language.
            - Updates global `current_language_settings`.
        """
        global current_language_settings
        self.get_name.save_name(name)

        lang_info = LANG_SETTINGS.get(selected_language_code)
        if not lang_info:
            return jsonify({"error": f"Language code '{selected_language_code}' is not supported."}), 400

        vosk_url = lang_info.get("vosk_model_url")
        vosk_model_local_path = lang_info.get("vosk_model_path")
        vosk_model_zip_name = lang_info.get("vosk_model_zip_name")

        vosk_zip_save_path = os.path.join(MODELS_DIR, vosk_model_zip_name)
        self.download_and_extract(vosk_url, vosk_zip_save_path, vosk_model_local_path)

        tts_voice_or_path = lang_info.get("tts_voice_name")
        self.get_language.save_language(selected_language_code)

        current_language_settings = {
            "language_code": selected_language_code,
            "vosk_model_name": vosk_model_local_path,
            "tts_voice_name": tts_voice_or_path
        }

        return redirect(url_for('home'))