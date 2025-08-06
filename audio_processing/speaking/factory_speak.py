from config import LANG_SETTINGS
from which_spoken import WhichSpoken
from data_storage.lang_handler import GetLanguage
from init_speaking import InitSpeaking
from utils.play_audio import play_audio
init_speaking = InitSpeaking()

spoken = WhichSpoken(init_speaking.init_pyttsx3, init_speaking.init_tts, play_audio=play_audio)
get_lang = GetLanguage

class FactorySpeak:
    """
    Factory class to choose and execute appropriate speech engine.
    """
    def __init__(self, speak_english, speak_other, get_lang):
        self.speak_english = speak_english
        self.speak_other = speak_other
        self.get_lang = get_lang

    def speak(self, msg):
        usr_lang = self.get_lang.load_language()
        lang = usr_lang.get('language', 'en-US')
        selected_lang = LANG_SETTINGS.get(lang)
        spoken_languague_model = selected_lang.get('tts_voice_name')

        if spoken_languague_model == "pyttsx3":
            return self.speak_english(msg)
        else:
            return self.speak_other(msg, spoken_languague_model)

factory_Speak = FactorySpeak(spoken.speak_english, spoken.speak_other_language, get_lang=get_lang)