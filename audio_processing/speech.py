import json
import vosk
import os
from config import AUDIO_SAMPLERATE, LANG_SETTINGS
from data_storage.database import save_language, load_language


vosk_cash = {}
def _get_vosk_model(file_path):
    global vosk_cach
    
    model = vosk_cash.get(file_path)
    if not model:
        model = vosk.Model(file_path)
        if model:
            vosk_cash[file_path] = model
            print(vosk_cash[file_path])
    return vosk_cash[file_path]

def speech_to_text(data):
    """Converts audio data to text using Vosk."""
    usr_lang = load_language()
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
        model =  _get_vosk_model(lang_vosk_path_ex)
        rec = vosk.KaldiRecognizer(model, AUDIO_SAMPLERATE)

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()
        if model:
            text = model
            return text if text else ""
    except Exception as e:
        print(f"Error with Vosk speech-to-text: {e}")
        return ""