#!/usr/bin/env python3
"""
Sarvam AI Voice Assistant
-------------------------

This script orchestrates the complete voice assistant workflow:
1. Record audio from the microphone
2. Convert speech to text using Sarvam AI API
3. Process text with Gemini for grammar correction and response
4. Convert Gemini's response to speech
5. Play the audio response

Usage:
    python main.py
"""

import os
import sys
from speech_to_text import record_audio, speech_to_text
from gemini import GeminiChatBot
from text_to_speech import text_to_speech, play_audio

def run_voice_assistant_loop():
    """Run the voice assistant in a continuous loop until interrupted"""
    print("\n===== Sarvam AI Voice Assistant =====")
    print("Press Ctrl+C at any time to exit\n")
    
    try:
        session_count = 0
        while True:
            session_count += 1
            print(f"\n----- Session {session_count} -----")
            
            # Step 1: Record audio
            print("Step 1: Recording audio...")
            if not record_audio():
                print("Error: Failed to record audio. Trying again...")
                continue
                
            # Step 2: Convert speech to text
            print("\nStep 2: Converting speech to text...")
            transcript = speech_to_text(check_file=False, language='en-US')
            if not transcript:
                print("Error: Failed to convert speech to text. Trying again...")
                continue
                
            # Step 3: Process with Gemini
            print("\nStep 3: Processing with Gemini...")
            try:
                chatbot = GeminiChatBot()
                gemini_response = chatbot.process_speech_text(transcript)
                print(f"Gemini response: {gemini_response}")
            except Exception as e:
                print(f"Error processing with Gemini: {e}")
                print("Make sure you have set your GEMINI_API_KEY environment variable")
                continue
                
            # Step 4: Convert response to speech
            print("\nStep 4: Converting response to speech...")
            audio_file = text_to_speech(gemini_response)
            if not audio_file:
                print("Error: Failed to convert text to speech. Trying again...")
                continue
                
            # Step 5: Play the audio response
            print("\nStep 5: Playing audio response...")
            play_audio(audio_file)
            
            print("\n----- Session complete -----")
            print("Ready for next interaction. Press Ctrl+C to exit.")
            
    except KeyboardInterrupt:
        print("\n\nExiting Sarvam AI Voice Assistant. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return False
        
    return True

def main():
    """Main entry point for the application"""
    run_voice_assistant_loop()
    print("Thank you for using Sarvam AI Voice Assistant!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """Main entry point for the application"""
    run_voice_assistant_loop()
    print("Thank you for using Sarvam AI Voice Assistant!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
