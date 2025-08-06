# from data_storage.setup_database import GetLanguage
# from TTS.api import TTS
# import os
# import simpleaudio as sd
# import torch
# import pyttsx3
# from utils.make_dir import make_Dir
# from TTS.utils.radam import RAdam
# from config import LANG_SETTINGS
# torch.serialization.add_safe_globals({'TTS.utils.radam.RAdam': RAdam})

# class InitSpeaking:
#     tts_cache = None  # كاش ثابت للكلاس كله

#     @staticmethod
#     def init_pyttsx3():
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[0].id)
#         return engine

#     @classmethod
#     def init_tts(cls, tts_model):
#         if not cls.tts_cache:
#             speaker = TTS(model_name=tts_model, progress_bar=False, gpu=False)
#             cls.tts_cache = speaker
#         return cls.tts_cache


# class WhichSpoken:
#     def __init__(self, init_pyttsx3, init_tts, play_audio):
#         self.init_tts = init_tts
#         self.init_pyttsx3 = init_pyttsx3
#         self.play_audio = play_audio

#     def speak_english(self, msg):
#             try:
#                 engine = self._init_pyttsx3()
#                 engine.say(msg)
#                 engine.runAndWait()
#             except Exception as e:
#                 print(f"Error with text-to-speech: {e}")

#     def speak_other_language(self, msg, spoken_languague_model):
        
#         speaker = self.init_tts(spoken_languague_model)
#         print(speaker)
#         AUDIO_DIR = make_Dir('audio')
#         print(AUDIO_DIR)
#         audio_path = os.path.join(AUDIO_DIR, 'hi.wav')
#         print(audio_path)
#         speaker.tts_to_file(text=msg, file_path='hi.wav')
#         self.play_audio('hi.wav')

# def play_audio(audio_path):
#     wave_obj = sd.WaveObject.from_wave_file(audio_path)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()

# init_spoken = InitSpeaking()
# spoken = WhichSpoken(init_spoken.init_pyttsx3, init_spoken.init_tts, play_audio)

# class FactorySpeak:
#     def __init__(self, speak_english, speak_other, get_lang):
#         self.speak_english = speak_english
#         self.speak_other = speak_other
#         self.get_lang = get_lang
#     def speak(self, msg):
#         """Converts text to speech and plays it."""
#         usr_lang = self.get_lang.load_language()
#         lang = usr_lang.get('language')
#         print(lang)
#         if not lang:
#             lang = "en-US"
#         selected_lang = LANG_SETTINGS.get(lang)
#         print(selected_lang)
#         spoken_languague_model = selected_lang.get('tts_voice_name')
#         print(spoken_languague_model)
#         if spoken_languague_model == "pyttsx3":
#             return self.speak_english(msg)
#         else:
#             return self.speak_other_language(msg, spoken_languague_model)
# get_lang = GetLanguage

# factory_Speak = FactorySpeak(spoken.speak_english, spoken.speak_other_language, get_lang=get_lang)