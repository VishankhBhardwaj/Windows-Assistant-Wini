## Wini – Windows Voice Assistant

Wini is a Windows desktop voice assistant that listens for a wake word, transcribes your speech, uses an LLM to understand your intent, and then controls your system or searches the web using a set of tools.

### Overview

At a high level, Wini:

- **Listens for "Hey WINI"** using Picovoice Porcupine.
- **Records your command** with a VAD-based recorder that stops when you finish speaking.
- **Transcribes audio** to text using OpenAI Whisper (via `transformers`).
- **Understands and acts** on the command using LangChain + a Groq-hosted Llama 3.3 model.
- **Speaks responses back** using Kokoro TTS.
- **Controls your system** (open apps/folders, adjust volume, etc.) and **performs web, Wikipedia, and weather searches** via tools.

### Project Structure

- **`main.py`**: Entry point. Creates a `voiceAssistant` instance and starts the wake-word loop.
- **`voice_assistant.py`**: Manages wake-word detection, audio recording, interaction with the LLM agent, and playback of responses.
- **`app.py`**: Defines the LangChain agent (`agent_call`) using Groq’s Llama model and tools (system controls, search, weather, etc.).
- **`stt.py`**: Speech-to-text using Whisper and text-to-speech generation using Kokoro TTS.
- **`recorder.py`**: Microphone recording with Silero VAD to automatically stop when you stop speaking.
- **`tools.py`**: LangChain tools for volume control, opening applications/folders, browser search, speaking text, and shutting down Wini.
- **`requirements.txt`**: Python dependencies.
- **`wake_words/`**: Porcupine wake-word model file(s) for "Hey WINI".
- **Audio files (`greet.wav`, `acknowledgment.wav`, `reply.wav`, `Shutdown.wav`, `output.wav`)**: Used for greeting, acknowledgments, synthesized replies, and recorded commands.

There is also a local `venv/` directory for the Python virtual environment (optional and not required if you use your own venv).

### Requirements

- **Python 3.10+** (recommended)
- **Windows** (the tools and `os.startfile` are Windows-oriented)
- A working **microphone** and audio output device
- All Python packages listed in `requirements.txt`
- Several external API and access keys (set via environment variables):
  - Groq API key (LLM)
  - Hugging Face token (Whisper / Kokoro)
  - Picovoice Porcupine access key (wake word)
  - OpenWeatherMap API key (weather)
  - Google Custom Search + API key (web search)

### Setup and Installation

1. **Clone the repository** (or copy the project folder).
2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with the required keys:

   ```text
   HF_TOKEN=YOUR_HF_TOKEN
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   PORCUPINE_ACCESS_KEY=YOUR_PORCUPINE_ACCESS_KEY
   ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY   # if used
   OPENWEATHERMAP_API_KEY=YOUR_OPENWEATHERMAP_API_KEY
   GOOGLE_CSE_ID=YOUR_GOOGLE_CUSTOM_SEARCH_ENGINE_ID
   GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
   ```

   Do **not** commit real keys to version control.

5. **Ensure wake-word model** file exists at `wake_words/Hey-WINI_en_windows_v4_0_0.ppn` or update the path in `voice_assistant.py`.

### Usage

1. Activate your virtual environment (if not already activated).
2. From the project root, run:

   ```bash
   python main.py
   ```

3. Wini will initialize the microphone and Porcupine, then listen for the wake word **“Hey WINI”**.
4. After Wini detects the wake word:
   - You’ll hear a greeting sound.
   - Speak your command (e.g., “open Chrome”, “increase volume”, “search weather in Delhi”, “open downloads”, etc.).
   - Wini will transcribe, call the LLM agent, and respond via speech.

Press `Ctrl+C` in the terminal to stop Wini; it will clean up audio resources and play a shutdown sound.

### Extending Wini

- Add new tools or system actions by defining additional `@tool` functions in `tools.py` and registering them in the tools list used by `agent_call` in `app.py`.
- You can customize prompts, models, or behavior inside `app.py` and `voice_assistant.py`.

### Notes

- This project uses online services (Groq, Hugging Face, OpenWeatherMap, Google, etc.). Make sure your machine has internet access when running Wini.
- For best performance with Whisper and Kokoro, a GPU is helpful but not required.
*** End of File

This repository contains the source code for the **Wini** project.

> Note: This README is a generic template. Update it with specific details about your project structure, features, and setup when available.

### Overview

Provide a brief description of what this project does, its main goals, and the problem it solves.

### Project Structure

Describe the important directories and files in this repository. For example:

- **`src/`**: Main source code.
- **`tests/`**: Automated tests.
- **`data/`**: Data files or datasets (if applicable).

Adjust these to match your actual structure.

### Requirements

List key tools and dependencies needed to work with this project, for example:

- **Python 3.x** or another runtime
- **Package manager** (e.g., `pip`, `npm`, `conda`) if applicable

Add exact versions when they are known.

### Setup and Installation

Provide step-by-step instructions to get the project running locally. For example:

1. Clone this repository.
2. Create and activate a virtual environment (if using Python).
3. Install dependencies.
4. Run the application or scripts.

Replace these steps with concrete commands once your environment is defined.

### Usage

Explain how to run the main scripts, services, or commands. Include example commands and expected behavior.

### Testing

Document how to run tests, if any. For example:

```bash
pytest
```

or the relevant command for your stack.

### Contributing

If others will contribute to this project, describe the contribution workflow (branching, coding style, code review, etc.).

### License

Add the license under which this project is distributed (e.g., MIT, Apache 2.0), or state that it’s private/internal if no open-source license applies.

