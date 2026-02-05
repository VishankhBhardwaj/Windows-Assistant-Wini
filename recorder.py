# import sounddevice as sd 
# from scipy.io.wavfile import write 

# def record_audio(filename, duration=5, samplerate=44100): 
#     print(f"Recording for {duration} seconds...") 
#     audio_data = sd.rec( int(samplerate * duration), samplerate=samplerate, channels=2, dtype="int16" ) 
#     sd.wait() # Wait until recording is finished 
#     write(filename, samplerate, audio_data) 
#     # Save as WAV file 
#     print(f"Recording saved to {filename}") 
#     return True 
# if __name__ == "__main__": 
#     record_audio("output.wav", duration=3, samplerate=44100) 
#     print("Audio recording complete.")
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import torch
from silero_vad import load_silero_vad
import os
from dotenv import load_dotenv
load_dotenv()

SAMPLE_RATE = 16000
FRAME_LENGTH = 512
SILENCE_LIMIT = 1.0
vad_model = load_silero_vad()
def record_audio(filename, duration=5, samplerate=44100): 
    frames = []
    silence_time = [0]
    def callback(indata, frame_count, time, status):
        pcm_float = indata[:, 0].astype(np.float32)
        audio_tensor = torch.FloatTensor(pcm_float)
        prob = vad_model(audio_tensor,SAMPLE_RATE).item()

        frames.append(pcm_float.copy())

        if prob < 0.2:
            silence_time[0] += frame_count / SAMPLE_RATE
        else:
            silence_time[0] = 0

        if silence_time[0] > SILENCE_LIMIT:
            raise sd.CallbackStop()
    print("Recording Started:-")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=FRAME_LENGTH,
        callback=callback
    ):
        sd.sleep(5000)

    audio = np.concatenate(frames)
    audio_int16 = (audio * 32767).astype(np.int16)
    write(filename, SAMPLE_RATE, audio_int16)
    return True
if __name__ == "__main__": 
    record_audio("Coice_commands/Command.wav", duration=3, samplerate=44100) 
    print("Audio recording complete.")
