import simpleaudio as sa
import os

def play_audio(audio_path):
    """
    Plays a .wav audio file using simpleaudio.
    
    Args:
        audio_path (str): Path to the .wav file.
    
    Returns:
        bool: True if playback was successful, False otherwise.
    """
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return False

    try:
        wave_obj = sa.WaveObject.from_wave_file(audio_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print("✅ Playback finished.")
        return True
    except Exception as e:
        print(f"⚠️ Error during playback: {e}")
        return False