# Wini – Windows Voice Assistant

Wini is an intelligent Windows desktop voice assistant that listens for a wake word, transcribes your speech using advanced AI models, understands your intent through a large language model, and executes system commands or searches the web—all through natural voice interaction.

## 🌟 Features

### Voice Interaction
- **Wake Word Detection**: Always-listening mode using Picovoice Porcupine for "Hey WINI" activation
- **Voice Activity Detection (VAD)**: Automatic speech detection using Silero VAD that stops recording when you finish speaking
- **Speech-to-Text**: High-accuracy transcription using OpenAI Whisper (large-v3) with GPU acceleration
- **Text-to-Speech**: Natural-sounding voice responses using Kokoro TTS with customizable voices

### AI-Powered Understanding
- **LLM Agent**: Powered by Groq's Llama 3.3 70B model for intelligent command interpretation
- **Context-Aware**: Handles spelling errors, filler words, and natural speech patterns
- **Tool Integration**: Automatically selects and executes the appropriate tool based on your request

### System Control Tools
- **Volume Control**: Increase, decrease, or mute system volume
- **Application Launcher**: Open any application, folder, file, or website
- **Folder Access**: Quick access to Downloads, Documents, Desktop, Pictures, Music, and Videos
- **Browser Integration**: Search the web or play music/videos directly

### Information Retrieval
- **Web Search**: DuckDuckGo and Google Custom Search integration
- **Wikipedia**: Quick facts and information lookup
- **Weather**: Real-time weather information for any city via OpenWeatherMap
- **Browser Search**: Direct YouTube and web searches

### Audio Feedback
- **Multiple Greetings**: Randomized greeting sounds for natural interaction
- **Acknowledgment Sounds**: Audio feedback when processing commands
- **Shutdown Sound**: Graceful exit notification

## 📁 Project Structure

```
Wini/
├── main.py                 # Entry point - initializes and starts the voice assistant
├── voice_assistant.py      # Core assistant logic: wake word detection, recording, LLM interaction
├── app.py                  # LangChain agent configuration with Groq LLM and tools
├── stt.py                  # Speech-to-text (Whisper) and text-to-speech (Kokoro) modules
├── recorder.py             # VAD-based audio recording with automatic silence detection
├── tools.py                # LangChain tool definitions for system control and actions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables and API keys (not committed)
├── Voice_commands/         # Pre-recorded audio files for greetings and responses
│   ├── greet1.wav
│   ├── greet2.wav
│   ├── greet3.wav
│   ├── acknowledgment.wav
│   ├── Shutdown.wav
│   ├── command.wav         # Recorded user command (temporary)
│   └── reply.wav           # Generated TTS response (temporary)
├── wake_words/             # Porcupine wake word model
│   └── Hey-WINI_en_windows_v4_0_0.ppn
└── reply.wav               # Generated TTS audio file
```

## 🛠️ Requirements

### System Requirements
- **Operating System**: Windows 10/11
- **Python**: 3.10 or higher (recommended)
- **Hardware**: 
  - Working microphone
  - Audio output device
  - GPU recommended for faster Whisper transcription (optional)

### API Keys Required
You'll need to obtain the following API keys:

1. **Groq API Key** - For LLM (Llama 3.3 70B)
   - Sign up at: https://console.groq.com
   
2. **Hugging Face Token** - For Whisper and Kokoro models
   - Sign up at: https://huggingface.co/settings/tokens
   
3. **Picovoice Porcupine Access Key** - For wake word detection
   - Sign up at: https://console.picovoice.ai
   
4. **OpenWeatherMap API Key** - For weather information
   - Sign up at: https://openweathermap.org/api
   
5. **Google Custom Search API** - For web search
   - Google API Key: https://console.cloud.google.com
   - Custom Search Engine ID: https://programmablesearchengine.google.com

## 🚀 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/VishankhBhardwaj/Windows-Assistant-Wini.git
cd Wini
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with PyTorch, install it separately:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with your API keys:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
PORCUPINE_ACCESS_KEY=your_porcupine_access_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id_here

# Optional (if using ElevenLabs instead of Kokoro)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

**⚠️ Important**: Never commit your `.env` file to version control!

### 5. Verify Wake Word Model
Ensure the wake word model exists at:
```
wake_words/Hey-WINI_en_windows_v4_0_0.ppn
```

If you need to create a custom wake word, visit [Picovoice Console](https://console.picovoice.ai).

## 💻 Usage

### Starting Wini

1. Activate your virtual environment:
```bash
venv\Scripts\activate
```

2. Run the assistant:
```bash
python main.py
```

3. Wait for the initialization message:
```
🎤 Listening for 'Hey WINI'...
Press Ctrl+C to stop
```

### Interacting with Wini

1. **Say the wake word**: "Hey WINI"
2. **Wait for the greeting sound** (confirms activation)
3. **Speak your command** naturally
4. **Wait for acknowledgment** (confirms command received)
5. **Listen to the response**

### Example Commands

**System Control:**
- "Open Chrome"
- "Increase volume"
- "Open Downloads folder"
- "Mute volume"

**Information Retrieval:**
- "Search for weather in Delhi"
- "What is artificial intelligence?" (Wikipedia)
- "Search for Python tutorials" (Web search)

**Media:**
- "Play Bohemian Rhapsody" (YouTube)
- "Search for relaxing music"

**Shutdown:**
- "Goodbye"
- "Shutdown"
- "Stop"

### Stopping Wini

Press `Ctrl+C` in the terminal. Wini will:
- Clean up audio resources
- Play a shutdown sound
- Exit gracefully

## 🔧 Technical Details

### Architecture Flow

```
User speaks "Hey WINI" 
    ↓
Porcupine detects wake word
    ↓
Play greeting sound
    ↓
Record audio with VAD (auto-stops on silence)
    ↓
Play acknowledgment sound
    ↓
Whisper transcribes audio to text
    ↓
LangChain agent (Llama 3.3) processes command
    ↓
Agent selects and executes appropriate tool
    ↓
Kokoro generates TTS response
    ↓
Play audio response to user
```

### Key Technologies

- **Wake Word**: Picovoice Porcupine (custom "Hey WINI" model)
- **VAD**: Silero VAD (automatic speech detection)
- **STT**: OpenAI Whisper large-v3 (via faster-whisper)
- **LLM**: Groq Llama 3.3 70B Versatile
- **TTS**: Kokoro ONNX (voice: af_heart)
- **Agent Framework**: LangChain with ZERO_SHOT_REACT_DESCRIPTION agent
- **Audio**: sounddevice, soundfile, numpy

### Agent Configuration

- **Model**: llama-3.3-70b-versatile
- **Temperature**: 0 (deterministic responses)
- **Max Iterations**: 2 (prevents infinite loops)
- **Agent Type**: ZERO_SHOT_REACT_DESCRIPTION
- **Error Handling**: Enabled with graceful fallbacks

## 🎨 Customization

### Adding New Tools

1. Define a new tool in `tools.py`:
```python
from langchain.tools import tool

@tool
def my_custom_tool(command: str) -> str:
    """Description of what this tool does"""
    # Your implementation
    return "Success message"
```

2. Register it in `app.py`:
```python
agent = initialize_agent(
    tools=[..., my_custom_tool],  # Add your tool here
    ...
)
```

### Changing TTS Voice

Edit `stt.py` line 33:
```python
generator = pipeline(reply, voice='af_heart')  # Change voice here
```

Available voices: Check Kokoro documentation for options.

### Adjusting Wake Word Sensitivity

Edit `voice_assistant.py` line 34:
```python
sensitivities=[0.8]  # Range: 0.0 to 1.0 (higher = more sensitive)
```

### Modifying VAD Settings

Edit `recorder.py`:
```python
SILENCE_LIMIT = 1.0  # Seconds of silence before stopping
```

## 🧪 Testing

Test individual components:

```bash
# Test speech-to-text and text-to-speech
python stt.py

# Test audio recording
python recorder.py

# Test imports and dependencies
python test_imports.py
```

## 🐛 Troubleshooting

### Common Issues

**1. "Wake word file not found"**
- Ensure `wake_words/Hey-WINI_en_windows_v4_0_0.ppn` exists
- Check the path in `voice_assistant.py`

**2. "CUDA out of memory"**
- Reduce Whisper model size in `stt.py`: Change `large-v3` to `medium` or `small`
- Or use CPU: Change `device="cuda"` to `device="cpu"`

**3. "No module named 'X'"**
- Reinstall requirements: `pip install -r requirements.txt`
- Check virtual environment is activated

**4. "API key error"**
- Verify all keys in `.env` are correct
- Ensure `.env` is in the project root
- Check for extra spaces or quotes in `.env`

**5. Microphone not detected**
- Check Windows audio settings
- Ensure microphone permissions are granted
- Try different microphone device index in `voice_assistant.py`

## 📝 Notes

- **Internet Required**: This project uses online services (Groq, Hugging Face, OpenWeatherMap, Google)
- **GPU Recommended**: For faster Whisper transcription, but CPU works fine
- **Privacy**: All voice processing happens locally except for LLM calls to Groq
- **Rate Limits**: Be aware of API rate limits for free tiers

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new tools and features
- Improve error handling
- Enhance documentation
- Report bugs or suggest improvements

## 📄 License

MIT License

Copyright (c) 2026 Vishankh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

- **Picovoice** for Porcupine wake word detection
- **OpenAI** for Whisper speech recognition
- **Groq** for fast LLM inference
- **Kokoro** for natural text-to-speech
- **LangChain** for agent framework
- **Silero** for voice activity detection

---

**Made with ❤️ by Vishankh**

For questions or support, please open an issue on GitHub.
