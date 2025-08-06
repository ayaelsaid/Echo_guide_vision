import queue
import sounddevice as sd
import vosk
from config import AUDIO_SAMPLERATE, AUDIO_BLOCKSIZE, AUDIO_CHANNELS, AUDIO_DTYPE

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Callback function for recording audio from the microphone."""
    audio_queue.put(bytes(indata))


def record_audio_once(duration_seconds):
    """Records audio for a specified duration."""
    print(f"🎤 Listening for {duration_seconds} seconds...")
    frames = []
    try:
        with sd.RawInputStream(samplerate=AUDIO_SAMPLERATE, blocksize=AUDIO_BLOCKSIZE,
                               dtype=AUDIO_DTYPE, channels=AUDIO_CHANNELS, callback=audio_callback):
            for _ in range(int(AUDIO_SAMPLERATE / AUDIO_BLOCKSIZE * duration_seconds)):
                try:
                    data = audio_queue.get(timeout=duration_seconds + 1)
                    frames.append(data)
                except queue.Empty:
                    print("Not enough audio data received within timeout.")
                    break
    except Exception as e:
        print(f"Error during audio recording: {e}")
        return b''

    if frames:
        return b''.join(frames)
    return b''