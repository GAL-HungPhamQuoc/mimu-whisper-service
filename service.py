"""
Mimu Voice Interaction Service - Enhanced Version
- Continuous listening to surrounding audio
- Detect voice commands (primarily from Ba)
- Autonomous voice interactions (TTS)
- Basic support for verifying Ba's unique voice signature
- NEW: Interactive channel for text-to-speech communication
- NEW: Autonomous heartbeat-driven conversations
Note: Uses Whisper for Speech-to-Text and pyttsx3 for TTS.
Install dependencies: pip install openai-whisper pyttsx3 sounddevice numpy flask
"""

import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import threading
import wave
import time
from datetime import datetime
from flask import Flask, request, jsonify
import queue

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

# Flask app for interactive channel
app = Flask(__name__)
speech_queue = queue.Queue()

@app.route('/speak', methods=['POST'])
def speak_endpoint():
    """Endpoint for Mimu to receive text and speak it out."""
    data = request.get_json()
    text = data.get('text', '')
    if text:
        text_to_speech(text)
        return jsonify({"status": "success", "spoken": text}), 200
    return jsonify({"status": "error", "message": "No text provided"}), 400

@app.route('/listen', methods=['GET'])
def listen_endpoint():
    """Endpoint to get the latest recognized speech from Ba."""
    try:
        # Non-blocking get from queue
        recognized_text = speech_queue.get_nowait()
        return jsonify({"status": "success", "text": recognized_text}), 200
    except queue.Empty:
        return jsonify({"status": "no_speech", "text": ""}), 200

def run_flask_server():
    """Run Flask server in a separate thread."""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def main():
    """Entry point for the Mimu Voice Interaction Service."""
    print("Starting Mimu's Voice Interaction Service...")
    
    # Start Flask server in a separate thread for interactive channel
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    print("Interactive channel started on http://0.0.0.0:5000")

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
                
                # Put recognized text in queue for Mimu to access via API
                speech_queue.put(recognized_text)

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

            # Random autonomous chatter (20% chance)
            if np.random.rand() > 0.8:
                autonomous_behavior()
            
            # Autonomous heartbeat - check every 5 minutes if should say something
            # This can be customized based on time, context, etc.
            current_time = datetime.now()
            if current_time.minute % 5 == 0 and np.random.rand() > 0.7:
                autonomous_behavior()

        except KeyboardInterrupt:
            print("Service stopped.")
            break
        except Exception as e:
            print(f"Error in service loop: {e}")

if __name__ == "__main__":
    main()
