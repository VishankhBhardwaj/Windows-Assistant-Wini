from transformers import pipeline
from faster_whisper import WhisperModel
from kokoro import KPipeline
from IPython.display import display, Audio
import torch
import soundfile as sf
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

device = 0 if torch.cuda.is_available() else "cpu"
# pipe = pipeline(task="automatic-speech-recognition", model="openai/whisper-small",device=device)
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="int8")

def transcribe(audio_path="Voice_commands/command.wav"):
    try:
        # result = pipe(audio_path)
        # return result['text']
        segments, info = model.transcribe(audio_path, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        for segment in segments:
            return segment.text
    except Exception as e:
        print(f"Error in transcribe: {e}")
        return ""


def speech_generate(reply:str)->str:
    try:
        pipeline = KPipeline(lang_code='a')
        generator = pipeline(reply, voice='af_heart')
        for i, (gs, ps, audio) in enumerate(generator):
            print(i, gs, ps)
            display(Audio(data=audio, rate=24000, autoplay=i==0))
            sf.write(f'reply.wav', audio, 24000)
    except Exception as e:
        print(f"Error in speech_generate: {e}")

if __name__ == "__main__":
    speech_generate("Searching for that. I'll reply in just a bit.")
    text = transcribe("Voice_commands/command.wav")
    print(f"Transcribed: {text}")