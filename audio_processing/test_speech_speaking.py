from audio_processing.speaking.init_speaking import InitSpeaking
from audio_processing.speaking.which_spoken import WhichSpoken
from utils.play_audio import play_audio
from audio_processing.speaking.factory_speak import FactorySpeak
from audio_processing.listen import Record
from audio_processing.speech import Stt

class GetLanguage:
    def load_language(self):
        return {"language": 'en-US'}

  get_lang = GetLanguage()
  init_speaking = InitSpeaking()
  spoken = WhichSpoken(init_speaking.init_pyttsx3, init_speaking.init_tts, play_audio=play_audio)
  factory_Speak = FactorySpeak(spoken.speak_english, spoken.speak_other_language, get_lang=get_lang)


def test_speech_record_speak():
    record = Record()
    data = record.record_audio_once(duration_seconds=4)

    stt = Stt()
    text = stt.speech_to_text('en-US', data)
    factory_Speak.speak(text)

test_speech_record_speak()    


def test_speak_output(text, lang_code):
    """
    Runs a full speech synthesis test using the FactorySpeak system.

    Args:
        text (str): The message to be spoken.
        lang_code (str): Language code.

    Side Effects:
        Plays the synthesized speech using the appropriate engine.
    """
    # Mock language loader
    class GetLanguage:
        def load_language(self):
            return {"language": lang_code}


    # Initialize components

    # Run the speech
    print(f"Speaking in {lang_code}: {text}")
    factory_Speak.speak(text)

test_speech_output("Hello, this is a test in English", lang_code="en-US")

