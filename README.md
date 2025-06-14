# Sarvam AI Voice Assistant

A conversational voice assistant that uses Sarvam AI's speech APIs and Google's Gemini AI to provide natural voice interactions.

## Overview

This project creates a full voice assistant pipeline:

1. **Audio Input**: Records voice from your microphone
2. **Speech-to-Text**: Converts speech to text using Sarvam AI's API
3. **AI Processing**: Processes text with Gemini to correct grammar and generate responses
4. **Text-to-Speech**: Converts Gemini's response to speech using Sarvam AI
5. **Audio Playback**: Plays the response through your speakers

## Features

- **Natural Language Processing**: Uses Gemini AI to understand and respond to queries
- **Grammar Correction**: Automatically fixes grammar issues in your speech
- **Voice Interaction**: Fully voice-based interface
- **Multi-language Support**: Configurable language settings (default: English)
- **Continuous Operation**: Runs indefinitely until manually stopped

## Requirements

- Python 3.12+
- uv package manager
- ALSA audio tools (for Linux)
- A Sarvam AI API key
- A Google Gemini API key

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd sarvam
```

### 2. Set up the environment with uv

```bash
# Initialize project structure
uv init

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv add pyaudio google-generativeai requests requests-toolbelt
```

### 3. Set up API keys

```bash
# Run the API key setup helper (recommended)
python setup_api_key.py

# Or manually set the Gemini API key
export GEMINI_API_KEY="your_gemini_api_key_here"

# The Sarvam API key is already in the code (995ca742-334f-4008-9f35-4f339425d395)
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key" if you don't have one already
4. Copy your API key and use it with the setup script

## Project Structure

- `main.py` - Main application entry point
- `audio.py` - Audio recording functionality
- `speech_to_text.py` - Converts speech to text using Sarvam AI
- `gemini.py` - Processes text with Gemini AI
- `text_to_speech.py` - Converts text to speech using Sarvam AI

## Usage

### Run the complete voice assistant

```bash
uv run main.py
```

The program will:
1. Prompt you to start speaking
2. Listen until you press 'q' and Enter
3. Process your speech and generate a response
4. Play the response through your speakers
5. Repeat until you press Ctrl+C to exit

### Run individual components

#### Record audio only

```bash
uv run audio.py
```

#### Convert speech to text only

```bash
uv run speech_to_text.py
```

#### Test Gemini AI with example inputs

```bash
uv run gemini.py
```

## Troubleshooting

### Audio Issues

If you encounter ALSA errors:

```
ALSA lib pcm_dmix.c:1000:(snd_pcm_dmix_open) unable to open slave
```

These are common warnings that usually don't affect functionality. If recording doesn't work:

1. Check your microphone is properly connected
2. Install ALSA tools: `sudo apt install alsa-utils`
3. Test your microphone: `arecord -d 5 test.wav`

### API Issues

- **Sarvam API errors**: Check your internet connection and verify the API key
- **Gemini API errors**: Ensure GEMINI_API_KEY is properly set in your environment

## License

[MIT License](LICENSE)

## Acknowledgments

- [Sarvam AI](https://api.sarvam.ai) for speech-to-text and text-to-speech APIs
- [Google Gemini](https://ai.google.dev/gemini-api) for text processing and conversation
