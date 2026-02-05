import pvporcupine
import pvrecorder
import os
import random
from recorder import record_audio
from stt import transcribe,speech_generate
from app import agent_call
from dotenv import load_dotenv
load_dotenv()


class voiceAssistant:
    def __init__(self):
        self.wake_word_path = "wake_words/Hey-WINI_en_windows_v4_0_0.ppn"
        self.porcupine = None
        self.recorder = None
        self.command = None
        self.final_command = None
        self.agent_reply = None
        self.greetings = [
            "Voice_commands/greet1.wav",
            "Voice_commands/greet2.wav",
            "Voice_commands/greet3.wav",
        ]
    def initialize(self):
        try:
            if not os.path.exists(self.wake_word_path):
                raise FileNotFoundError(f"❌ Wake word file not found: {self.wake_word_path}")
        
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keyword_paths=[self.wake_word_path], # Built-in keywords
            sensitivities=[0.8]
            )
            #Initialize recorder
            self.recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
            return True
        except Exception as e:
            print("Initialization failed",e)
            return False
    
    def start(self):
        if not self.initialize():
            return
        print("\n🎤 Listening for 'Hey WINI'...")
        print("Press Ctrl+C to stop\n")
        self.recorder.start()
        try:
            while True:
                pcm = self.recorder.read()
                # Process audio frame
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Detected Keyword")
                    self.speak(random.choice(self.greetings))
                    reply = record_audio("Voice_commands/Command.wav", duration=10, samplerate=44100)
                    print("here",reply)
                    if(reply):
                        self.speak("Voice_commands/acknowledgment.wav")
                        self.command = transcribe("Voice_commands/command.wav")
                        print(self.command)
                        response = self.invoke_llm()
                        print(f"Final response is as follows:-{response}")
                        self.speak_text(response)
                    else:
                        print("Something went wrong")
        except KeyboardInterrupt:
            print("\n⏹️ Stopping...")
        except Exception as e:
            print("Error occured",e)
        finally:
            self.cleanup()


    def speak_text(self,text: str) -> str:
        """
        Convert text to speech and immediately play it.
        Combines TTS generation and audio playback.
        """
        # Generate audio
        speech_generate(text)

        # Play audio
        import sounddevice as sd
        import soundfile as sf
        data, fs = sf.read("reply.wav", dtype='float32')
        sd.play(data, fs)
        sd.wait()

        return "✅ Spoken response played"

    def invoke_llm(self):
        try:
            self.agent_reply = agent_call(self.command)
            return self.agent_reply
        except Exception as e:
            print(f"Some error occured:-{e}")
            return
    def speak(self,file_path:str)->str:
        import sounddevice as sd
        import soundfile as sf
        data, fs = sf.read(file_path, dtype='float32')
        sd.play(data, fs)
        sd.wait()
    def cleanup(self):
        import sys
        if self.recorder is not None:
            self.recorder.stop()
            self.recorder.delete()
        if self.porcupine is not None:
            self.porcupine.delete()
        self.speak("Voice_commands/Shutdown.wav")
        print("Cleaned up everything bye bye :)")
        sys.exit()
    



    







