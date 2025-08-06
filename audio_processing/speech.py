import json
import vosk
import os
from config import AUDIO_SAMPLERATE, LANG_SETTINGS

class Stt:
    """
    A class for performing speech-to-text conversion using Vosk.

    Attributes:
        vosk_cache (dict): Class-level cache for loaded Vosk models.
        get_lang (Get_language): Instance used to retrieve the user's selected language.
    """

    vosk_cache = {}

    def __init__(self, get_lang):
        """
        Initializes the Stt class with a language retriever.

        Args:
            get_lang (Get_language): Object that provides the user's language settings.
        """
        self.get_lang = get_lang

    @classmethod
    def _get_vosk_model(cls, file_path):
        """
        Loads and caches a Vosk model from the given path.

        Args:
            file_path (str): Path to the Vosk model directory.

        Returns:
            vosk.Model: Loaded Vosk model instance.
        """
        model = cls.vosk_cache.get(file_path)
        if not model:
            model = vosk.Model(file_path)
            cls.vosk_cache[file_path] = model
            print(f"Model cached for: {file_path}")
        return model

    def speech_to_text(self, data):
        """
        Converts raw audio data to text using the appropriate Vosk model.

        Args:
            data (bytes): Raw audio data in WAV format.

        Returns:
            str: Transcribed text from the audio input. Returns an empty string on failure.
        """
        usr_lang = self.get_lang.load_language()
        lang = usr_lang.get('language')
        print(lang)
        if not lang:
            lang = "en-US"

        selected_lang = LANG_SETTINGS.get(lang)
        print(selected_lang)
        lang_vosk_path = selected_lang.get('vosk_model_path')
        print(lang_vosk_path)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        lang_vosk_path_ex = os.path.join(BASE_DIR, lang_vosk_path)
        print(lang_vosk_path_ex)

        if not os.path.exists(lang_vosk_path_ex):
            print(f"Error: Vosk model not found at {lang_vosk_path_ex}. Please download it.")
            return ""
        else:
            print(f"Vosk model found at {lang_vosk_path_ex}")

        try:
            model = self._get_vosk_model(lang_vosk_path_ex)
            if model:
                rec = vosk.KaldiRecognizer(model, AUDIO_SAMPLERATE)

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    return text if text else ""
        except Exception as e:
            print(f"Error with Vosk speech-to-text: {e}")
            return ""