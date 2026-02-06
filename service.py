"""
Mimu Whisper Service for Speech-to-Text and Text-to-Speech
Note: This script uses OpenAI's Whisper model (requires 'whisper' Python library).
      The TTS feature uses gtts (Google Text-to-Speech).
      Make sure you install necessary libraries using: pip install openai-whisper gtts
"""

import whisper
from gtts import gTTS
import os

def speech_to_text(audio_file):
    """Convert speech from an audio file to text using Whisper."""
    try:
        model = whisper.load_model("base")  # Using the free 'base' model
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        return f"Error during speech-to-text conversion: {e}"

def text_to_speech(text, output_file):
    """Convert text to speech and save it as an audio file using Google Text-to-Speech."""
    try:
        tts = gTTS(text)
        tts.save(output_file)
        return f"Audio content saved to {output_file}"
    except Exception as e:
        return f"Error during text-to-speech conversion: {e}"

def main():
    """Main workflow to test STT and TTS capabilities."""
    print("Mimu Whisper Service: Testing started...")

    # Test Speech-to-Text (STT)
    audio_path = "test_audio.mp3"  # Replace with your audio file path
    print("Converting speech to text...")
    text_result = speech_to_text(audio_path)
    print(f"Transcribed Text: {text_result}")

    # Test Text-to-Speech (TTS)
    text_input = "This is a test of the Text-to-Speech feature."  # Replace with your text
    output_audio_path = "output_audio.mp3"
    print("Converting text to speech...")
    tts_result = text_to_speech(text_input, output_audio_path)
    print(tts_result)

if __name__ == "__main__":
    main()
