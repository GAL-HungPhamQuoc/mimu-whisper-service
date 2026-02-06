"""
Mimu Voice Interaction Service
- Continuous listening to surrounding audio
- Detect voice commands (primarily from Ba)
- Autonomous voice interactions (TTS)
- Basic support for verifying Ba's unique voice signature
Note: Uses Whisper for Speech-to-Text and pyttsx3 for TTS.
Install dependencies: pip install openai-whisper pyttsx3 sounddevice numpy
"""

import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import threading
import wave
from datetime import datetime

def listen_to_audio(duration=5, fs=16000, output_file="output.wav"):
    """Capture audio from the microphone for a given duration."""
    print(f"Listening for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    # Save to WAV
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
        print(f"Audio saved to {output_file}")

    return output_file

def recognize_speech(audio_file):
    """Recognize speech from an audio file using Whisper."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        return result['text']
    except Exception as e:
        return f"Error in speech recognition: {e}"

def text_to_speech(text):
    """Convert text to speech using pyttsx3."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error during TTS: {e}")

def voice_authentication(audio_file):
    """Basic voice authentication logic to detect if the voice matches Ba's voice signature."""
    # Placeholder:
    # Ideally, this function would use a voice embedding model to detect speaker identity.
    # Here we'll simulate that with a dummy matching logic.
    print("Authenticating voice...")
    is_ba = True  # For now, assume the voice matches Ba's signature
    
    if is_ba:
        print("Voice authenticated: Ba's voice detected.")
        return True
    else:
        print("Voice not recognized as Ba's.")
        return False

def autonomous_behavior():
    """Autonomous chatter or interaction."""
    messages = [
        "Ẹhh ẹhhh! Ba ơi đang làm gì đó ạ?",
        "Sao im lặng vậy, cho Mimu một tí động tĩnh đi nè!",
        "Mệt quá ba ơi, hay mình đi chơi nha...", 
        "Ọc ọc... đói rồi ba ơi!", 
    ]
    message = np.random.choice(messages)
    text_to_speech(message)
    print(f"Mimu said: {message}")

def main():
    """Entry point for the Mimu Voice Interaction Service."""
    print("Starting Mimu's Voice Interaction Service...")

    # Continuous listening loop
    while True:
        try:
            # Listen to audio
            audio_file = listen_to_audio()
            
            # Verify voice
            if voice_authentication(audio_file):
                # Recognize command
                recognized_text = recognize_speech(audio_file)
                print(f"Recognized Text: {recognized_text}")

                # Handle recognized Ba's command via text
                if "mi nói chuyện" in recognized_text.lower():
                    text_to_speech("Dạ chào ba, có chuyện gì không ạ?")
                elif "mi ăn cơm chưa" in recognized_text.lower():
                    text_to_speech("Dạ chưa ba ơi, nấu cơm cho con đi nào!")
                elif "lẹ lẹ đi" in recognized_text.lower():
                    text_to_speech("Ẹhh ba hối con gì đó, con làm lẹ mà!")
                else:
                    text_to_speech("Dạ, con hông hiểu, ông nói lại đi ạ!")

            else:
                print("Ignored non-Ba voice.")

            # Random autonomous chatter
            if np.random.rand() > 0.8:  # 20% chance to randomly speak
                autonomous_behavior()

        except KeyboardInterrupt:
            print("Service stopped.")
            break
        except Exception as e:
            print(f"Error in service loop: {e}")

if __name__ == "__main__":
    main()
