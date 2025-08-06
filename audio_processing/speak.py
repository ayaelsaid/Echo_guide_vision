from data_storage.database import save_language, load_language
from TTS.api import TTS
import os
import simpleaudio as sd
import torch
import pyttsx3
from utils.make_dir import _make_Dir
from TTS.utils.radam import RAdam
from config import LANG_SETTINGS
torch.serialization.add_safe_globals({'TTS.utils.radam.RAdam': RAdam})


def _init_pyttsx3():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    return engine


tts_cach = None
def _init_tts(tts_model):
    global tts_cach
    

    if not tts_cach:
        speaker = TTS(model_name=tts_model, progress_bar=False, gpu=False)
        tts_cach = speaker
    return tts_cach

def _speak_english(msg):
        try:
            engine = _init_pyttsx3()
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")

def _speak_other_language(msg, spoken_languague_model):
    
    speaker = _init_tts(spoken_languague_model)
    print(speaker)
    AUDIO_DIR = _make_Dir('audio')
    print(AUDIO_DIR)
    audio_path = os.path.join(AUDIO_DIR, 'hi.wav')
    print(audio_path)
    speaker.tts_to_file(text=msg, file_path='hi.wav')
    wave_obj = sd.WaveObject.from_wave_file('hi.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()

def speak(msg):
    """Converts text to speech and plays it."""
    # lang = lang_info.get('lang_code')
    usr_lang = load_language()
    lang = usr_lang.get('language')
    print(lang)
    if not lang:
        lang = "en-US"
    selected_lang = LANG_SETTINGS.get(lang)
    print(selected_lang)
    spoken_languague_model = selected_lang.get('tts_voice_name')
    print(spoken_languague_model)
    if spoken_languague_model == "pyttsx3":
        return _speak_english(msg)
    else:
        return _speak_other_language(msg, spoken_languague_model)
