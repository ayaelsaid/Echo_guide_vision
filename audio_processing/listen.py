import queue
import sounddevice as sd
import vosk
from config import AUDIO_SAMPLERATE, AUDIO_BLOCKSIZE, AUDIO_CHANNELS, AUDIO_DTYPE

class Record:
    """
    A class for recording raw audio input from the microphone using sounddevice.

    Attributes:
        audio_queue (queue.Queue): A thread-safe queue to store incoming audio chunks.
    """

    def __init__(self):
        """
        Initializes the Record object and sets up the audio queue.
        """
        self.audio_queue = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        """
        Callback function triggered by sounddevice during audio input.

        Args:
            indata (bytes): Raw audio input data.
            frames (int): Number of frames in this block.
            time (CData): Timestamps for the audio block.
            status (CallbackFlags): Status flags indicating stream state.

        Side Effects:
            Puts the raw audio bytes into the audio queue for later processing.
        """
        self.audio_queue.put(bytes(indata))

    def record_audio_once(self, duration_seconds):
        """
        Records audio from the microphone for a specified duration.

        Args:
            duration_seconds (int): Duration of recording in seconds.

        Returns:
            bytes: Concatenated raw audio data recorded during the session.
                   Returns empty bytes if recording fails or no data is received.

        Side Effects:
            Prints status messages to the console during recording.
        """
        print(f"🎤 Listening for {duration_seconds} seconds...")
        frames = []
        try:
            with sd.RawInputStream(
                samplerate=AUDIO_SAMPLERATE,
                blocksize=AUDIO_BLOCKSIZE,
                dtype=AUDIO_DTYPE,
                channels=AUDIO_CHANNELS,
                callback=self.audio_callback
            ):
                for _ in range(int(AUDIO_SAMPLERATE / AUDIO_BLOCKSIZE * duration_seconds)):
                    try:
                        data = self.audio_queue.get(timeout=duration_seconds + 1)
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