import requests
import base64
import subprocess
import os

def text_to_speech(text, output_file="gemini_response.wav", language_code="en-IN", api_key=None):
    """
    Convert text to speech using Sarvam AI API
    
    Args:
        text: The text to convert to speech
        output_file: The output audio file path
        language_code: The target language code (e.g., 'en-IN', 'hi-IN')
        api_key: The Sarvam API key (optional, defaults to environment variable)
    
    Returns:
        The path to the generated audio file or None if an error occurred
    """
    print("=== Converting Text to Speech ===")
    try:
        # Use provided API key or get from environment
        sarvam_api_key = api_key or os.getenv('SARVAM_API_KEY') or "995ca742-334f-4008-9f35-4f339425d395"
        
        response = requests.post(
            "https://api.sarvam.ai/text-to-speech",
            headers={
                "api-subscription-key": sarvam_api_key
            },
            json={
                "text": text,
                "target_language_code": language_code
            },
        )
        
        # Process the response
        result = response.json()
        
        if 'audios' in result and len(result['audios']) > 0:
            # Get the base64 encoded audio
            audio_base64 = result['audios'][0]
            
            # Decode the base64 audio
            audio_data = base64.b64decode(audio_base64)
            
            # Save the audio file
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"Response audio saved as {output_file}")
            return output_file
        else:
            print("Error: No audio data received")
            print(result)
            return None
            
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        return None

def play_audio(audio_file):
    """
    Play an audio file using available audio players
    
    Args:
        audio_file: The path to the audio file to play
        
    Returns:
        True if playback was successful, False otherwise
    """
    if not os.path.exists(audio_file):
        print(f"Error: Audio file {audio_file} not found")
        return False
        
    print(f"=== Playing Audio: {audio_file} ===")
    try:
        # Try different audio players based on availability
        if os.system("which aplay > /dev/null 2>&1") == 0:
            # Use aplay (ALSA)
            subprocess.run(["aplay", audio_file])
            return True
        elif os.system("which paplay > /dev/null 2>&1") == 0:
            # Use paplay (PulseAudio)
            subprocess.run(["paplay", audio_file])
            return True
        elif os.system("which ffplay > /dev/null 2>&1") == 0:
            # Use ffplay (ffmpeg)
            subprocess.run(["ffplay", "-nodisp", "-autoexit", audio_file])
            return True
        else:
            print("No audio player found. Install alsa-utils, pulseaudio-utils, or ffmpeg to play audio.")
            print(f"You can manually play the file: {audio_file}")
            return False
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

# When this file is run directly
if __name__ == "__main__":
    from gemini import main as gemini_main
    
    try:
        # Get response from Gemini
        gemini_response = gemini_main()
        
        if gemini_response:
            # Convert to speech
            audio_file = text_to_speech(gemini_response)
            
            # Play the audio
            if audio_file:
                play_audio(audio_file)
                print(f"Gemini said: {gemini_response}")
        else:
            print("No response from Gemini.")
    except Exception as e:
        print(f"An error occurred: {e}")