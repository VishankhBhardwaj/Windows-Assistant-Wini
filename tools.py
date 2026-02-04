from langchain.tools import tool
import os
import subprocess
import pyautogui
import time
import numpy as np
import webbrowser
from stt import speech_generate
@tool
def increase_volume(command: str) -> str:
    """Increase the system volume"""

    # Press volume up key multiple times
    for _ in range(5):
        pyautogui.press("volumeup")
        time.sleep(0.05)

    return "🔊 Volume increased"


@tool
def open_application(target: str) -> str:
    """
    Open any application, folder, file, or website on Windows using the system default handler.
    Use this tool when the user asks to open, launch, start, or access something.
    The input should be a short name, path, or URL (for example: 'chrome', 'Downloads', 'C:\\Users', 'https://google.com').
    """
    import os
    os.startfile(target)
    return f"Opened {target}"

@tool
def browser_search(search:str)->str:
    """
    Search on browser or Play music by opening a YouTube or Spotify link in the browser.

    Use this tool when the user asks to play music, songs, artists, albums, or playlists or search something on browser.
    The input must be a COMPLETE and VALID URL.

    Behavior rules for the agent:
    - If the user request is for a specific song or video, generate a direct YouTube watch URL.
    - If the request is generic (artist, genre, mood, playlist), generate a YouTube search URL.
    - Return ONLY the URL as input to this tool. Do not include explanations or extra text.
    """
    url = f"{search}"
    webbrowser.open(url)
@tool
def open_folder(command:str) -> str:
    """
    Open a common system folder.
    Allowed values: downloads, documents, desktop, pictures, music, videos
    """
    FOLDERS = {
        "downloads": os.path.expanduser("~/Downloads"),
        "documents": os.path.expanduser("~/Documents"),
        "desktop": os.path.expanduser("~/Desktop"),
        "pictures": os.path.expanduser("~/Pictures"),
        "music": os.path.expanduser("~/Music"),
        "videos": os.path.expanduser("~/Videos"),
    }
    folder = command.lower().strip()
    if folder not in FOLDERS:
        return "I don't know that folder.Please try again"
    os.startfile(FOLDERS[folder])
    return f"📁{folder} opened"

@tool
def mute_volume(command: str) -> str:
    """Mute or unmute the system volume"""

    pyautogui.press("volumemute")
    return "🔇 Volume toggled"

@tool
def decrease_volume(command:str) ->str:
    """Decrease the system volume"""
    for i in range(5):
        pyautogui.press("volumedown")
        time.sleep(0.05)

@tool
def text_to_speech_tool(text: str) -> str:
    """
    Convert text to speech using Kokoro TTS and save/play audio.

    Usage:
    1. Pass the text to be spoken.
    2. The speech_generate function will create the audio file '0.wav'.
    3. Use 'reply_to_user' tool to play the audio.
    """
    # Use existing function to generate TTS
    speech_generate(text)

    return "✅ Audio generated. Use reply_to_user to play it."

@tool
def speak_text(text: str) -> str:
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
@tool
def good_bye(command:str)->str:
    """
    Shutdown service
    Use this tool when user asks you to stop,shutdown,or says bye-bye or something like that
    """
    from voice_assistant import voiceAssistant
    assistant = voiceAssistant()
    assistant.cleanup()
    return "Wini shutdown successful"



