import os
from config import AUDIO_DIR
class WhichSpoken:
    """
    Handles speech synthesis based on the selected engine and language.

    This class supports:
    - English speech using pyttsx3 (offline, lightweight)
    - Multilingual speech using Coqui TTS (model-based)

    Args:
        init_pyttsx3 (Callable): Function to initialize pyttsx3 engine.
        init_tts (Callable): Function to initialize Coqui TTS engine with a model name.
        play_audio (Callable): Function to play a WAV audio file.
    """

    def __init__(self, init_pyttsx3, init_tts, play_audio):
        """
        Initializes the WhichSpoken class with engine initializers and audio playback.

        Args:
            init_pyttsx3 (Callable): Function to initialize pyttsx3.
            init_tts (Callable): Function to initialize TTS engine.
            play_audio (Callable): Function to play audio from a file.
        """
        self.init_tts = init_tts
        self.init_pyttsx3 = init_pyttsx3
        self.play_audio = play_audio

    def speak_english(self, msg):
        """
        Speaks the given message using the pyttsx3 engine.

        Args:
            msg (str): The text message to be spoken in English.

        Side Effects:
            Plays the spoken message using the system's default voice.
        """
        try:
            engine = self.init_pyttsx3()
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")

    def speak_other_language(self, msg, spoken_languague_model):
        """
        Speaks the given message using a multilingual TTS model.

        Args:
            msg (str): The text message to be spoken.
            spoken_languague_model (str): The name of the TTS model to use.

        Side Effects:
            Saves the generated speech to a WAV file and plays it.
        """
        speaker = self.init_tts(spoken_languague_model)
        audio_path = os.path.join(AUDIO_DIR, 'hi.wav')
        speaker.tts_to_file(text=msg, file_path=audio_path)
        self.play_audio(audio_path)