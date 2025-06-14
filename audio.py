import pyaudio
import wave
import subprocess
import os
import threading
import time

class AudioRecorder:
    def __init__(self, filename="audio_input.wav"):
        self.filename = filename
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        
        # Audio recording parameters
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        
    def start_recording(self):
        """Start recording audio"""
        print("Starting recording... Press 'q' and Enter to stop.")
        self.is_recording = True
        
        # Start recording in a separate thread
        recording_thread = threading.Thread(target=self._record_audio)
        recording_thread.start()
        
        # Wait for user input to stop recording
        while True:
            user_input = input()
            if user_input.lower() == 'q':
                self.stop_recording()
                break
                
        recording_thread.join()
        
    def _record_audio(self):
        """Internal method to handle audio recording"""
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        
        while self.is_recording:
            data = stream.read(self.chunk)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        # Save directly as WAV
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            
        print(f"Audio saved as {self.filename}")
            
        # # Convert WAV to MP3
        # self._convert_to_mp3()
        
    def stop_recording(self):
        """Stop recording audio"""
        print("Stopping recording...")
        self.is_recording = False
        
    # def _convert_to_mp3(self):
    #     """Convert WAV file to MP3 using ffmpeg"""
    #     try:
    #         # Use ffmpeg to convert WAV to MP3
    #         subprocess.run([
    #             'ffmpeg', '-i', self.temp_wav, 
    #             '-codec:a', 'libmp3lame', 
    #             '-b:a', '192k', 
    #             self.filename, '-y'
    #         ], check=True, capture_output=True)
            
    #         # Remove temporary WAV file
    #         os.remove(self.temp_wav)
    #         print(f"Audio saved as {self.filename}")
            
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error converting to MP3: {e}")
    #         print("Make sure ffmpeg is installed on your system")
    #     except FileNotFoundError:
    #         print("ffmpeg not found. Please install ffmpeg to convert to MP3")
    #         print("Keeping WAV file instead...")
    #         os.rename(self.temp_wav, self.filename.replace('.mp3', '.wav'))
            
    def __del__(self):
        """Cleanup PyAudio"""
        if hasattr(self, 'audio'):
            self.audio.terminate()

if __name__ == "__main__":
    recorder = AudioRecorder("audio_input.wav")
    
    try:
        recorder.start_recording()
    except KeyboardInterrupt:
        print("\nRecording interrupted by user")
        recorder.stop_recording()
    except Exception as e:
        print(f"An error occurred: {e}")