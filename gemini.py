import google.generativeai as genai
import os
import json
from speech_to_text import speech_to_text


class GeminiChatBot:
    def __init__(self, api_key=None):
        # Configure Gemini API
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # You can set your API key as environment variable
            # export GEMINI_API_KEY="your_api_key_here"
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompt for the chatbot
        self.system_prompt = """You are a helpful and friendly AI assistant. Your task is to:

1. First, identify and correct any grammar, spelling, or sentence structure errors in the user's input
2. Then respond naturally to the corrected message, continuing the conversation in a helpful and empathetic way

Follow this format:
- If there are errors: Start with "I think you meant: '[corrected sentence]'" 
- Then provide your response to the corrected message
- If no errors: Just respond naturally to the message

Be conversational, empathetic, and ask follow-up questions when appropriate. Keep responses concise but warm."""

    def process_speech_text(self, speech_text):
        """
        Process speech-to-text output and generate a response
        """
        try:
            # Create the full prompt
            full_prompt = f"""{self.system_prompt}

User said: "{speech_text}"

Please correct any errors first, then respond naturally."""

            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def chat(self, message):
        """
        Simple chat method for direct conversation
        """
        return self.process_speech_text(message)

def main():
    # Example usage
    chatbot = GeminiChatBot()
    
    # Test with some examples
    print("Getting speech-to-text...")
    message = speech_to_text()  # Call the function
    print(f"Speech input: '{message}'")
  
    
    print("=== Gemini Speech-to-Text Chatbot Demo ===\n")
    
    response = chatbot.process_speech_text(message)
    print(f"Gemini: {response}")
    
    print("-" * 50)
    return response
    # # Interactive mode
    # print("\n=== Interactive Mode ===")
    # print("Type 'quit' to exit")
    
    # while True:
    #     user_input = input("\nYou: ")
    #     if user_input.lower() == 'quit':
    #         break
        
    #     response = chatbot.chat(user_input)
    #     print(f"Bot: {response}")

if __name__ == "__main__":
    main()
