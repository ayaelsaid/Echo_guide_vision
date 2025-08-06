from TTS.api import TTS
import pyttsx3
from TTS.utils.radam import RAdam
import torch

# Ensure custom optimizer class is safely deserializable
torch.serialization.add_safe_globals({'TTS.utils.radam.RAdam': RAdam})

class InitSpeaking:
    """
    A utility class for initializing and caching text-to-speech (TTS) engines.

    This class supports both:
    - `pyttsx3`: A lightweight, offline TTS engine for English.
    - `TTS`: A more advanced multilingual engine from the Coqui TTS library.

    Attributes:
        tts_cache (TTS): A class-level cache for the TTS engine to avoid reloading the model multiple times.
    """

    tts_cache = None  # Shared cache across all instances

    @staticmethod
    def init_pyttsx3():
        """
        Initializes the pyttsx3 engine for English speech synthesis.

        Returns:
            pyttsx3.Engine: Configured speech engine with default voice.
        """
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        return engine

    @classmethod
    def init_tts(cls, tts_model):
        """
        Initializes and caches the Coqui TTS engine for multilingual speech synthesis.

        Args:
            tts_model (str): The name of the TTS model to load (e.g., 'tts_models/ar/mai_tts').

        Returns:
            TTS: An instance of the TTS engine, cached after first initialization.
        """
        if not cls.tts_cache:
            speaker = TTS(model_name=tts_model, progress_bar=False, gpu=False)
            cls.tts_cache = speaker
        return cls.tts_cache