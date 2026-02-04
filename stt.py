from transformers import pipeline
from kokoro import KPipeline
from IPython.display import display, Audio
import torch
import soundfile as sf
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")

device = 0 if torch.cuda.is_available() else "cpu"
pipe = pipeline(task="automatic-speech-recognition", model="openai/whisper-small",device=device)



def transcribe(audio_path="output.wav"):
    result = pipe(audio_path)
    return result['text']


def speech_generate(reply:str)->str:
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(reply, voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        display(Audio(data=audio, rate=24000, autoplay=i==0))
        sf.write(f'reply.wav', audio, 24000)

if __name__ == "__main__":
    speech_generate("Searching for that. I'll reply in just a bit.")
    # text = transcribe("output.wav")
    # print(f"Transcribed: {text}")