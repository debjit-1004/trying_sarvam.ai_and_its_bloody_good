import requests
import os
from audio import AudioRecorder
from requests_toolbelt.multipart.encoder import MultipartEncoder

def record_audio():
    """Record audio using the AudioRecorder class"""
    print("=== Recording Audio ===")
    recorder = AudioRecorder("audio_input.wav")
    
    try:
        recorder.start_recording()
        return True
    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
        recorder.stop_recording()
        return False
    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return False

def speech_to_text(check_file=True, language='en-US'):
    """
    Convert audio file to text using the Sarvam API
    
    Args:
        check_file: If True, verify the audio file exists before proceeding
        language: The source language code (e.g., 'en-US', 'hi-IN')
    """
    # Check if the audio file exists
    if check_file and not os.path.exists('audio_input.wav'):
        print("Error: audio_input.wav file not found.")
        print("Please record audio first using record_audio() function.")
        return None
        
    # Speech to Text (POST /speech-to-text)
    try:
        print("=== Converting Speech to Text ===")
        print(f"Using language: {language}")
        
        # Create multipart form data with both file and language parameters
        with open('audio_input.wav', 'rb') as f:
            audio_data = f.read()
            
        multipart_data = MultipartEncoder(
            fields={
                'file': ('audio_input.wav', audio_data, 'audio/wav'),
                'source_language_code': language
            }
        )
        
        # Get the API key from environment variable
        api_key = os.getenv('SARVAM_API_KEY')
        if not api_key:
            print("Error: SARVAM_API_KEY environment variable not set.")
            return None

        # Make the request with the custom content type
        response = requests.post(
            "https://api.sarvam.ai/speech-to-text",
            headers={
                "api-subscription-key": api_key,
                "Content-Type": multipart_data.content_type
            },
            data=multipart_data
        )

        data = response.json()
        # Format and return the response value
        result = data.get('transcript', data)
        print(f"Speech-to-text result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in speech-to-text conversion: {e}")
        return None

def record_and_convert(language='en-US'):
    """Record audio and then convert it to text"""
    if record_audio():
        return speech_to_text(check_file=False, language=language)
    else:
        return None

# When this file is run directly
if __name__ == "__main__":
    result = record_and_convert()
    if result:
        print(f"Final transcript: {result}")
    else:
        print("Failed to get speech-to-text result")
