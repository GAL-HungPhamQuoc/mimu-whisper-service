# Mimu Voice Interaction Service 🐱🎙️

Enhanced voice interaction service for Mimu AI with autonomous conversations and interactive TTS channel.

## Features

- 🎤 **Continuous Audio Listening**: Captures audio from microphone
- 🗣️ **Speech-to-Text**: Uses Whisper for accurate Vietnamese speech recognition
- 🔊 **Text-to-Speech**: Converts text to natural speech using pyttsx3
- 🎭 **Voice Authentication**: Basic speaker verification (Ba's voice)
- 🤖 **Autonomous Conversations**: Proactive speech triggered by heartbeat logic
- 🌐 **Interactive API**: Flask endpoints for programmatic interaction

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Mimu Voice Service                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Mic Input  │────────>│   Whisper    │             │
│  │  (Ba's voice)│         │     STT      │             │
│  └──────────────┘         └──────┬───────┘             │
│                                   │                      │
│                                   v                      │
│                          ┌────────────────┐             │
│                          │  Speech Queue  │             │
│                          └────────┬───────┘             │
│                                   │                      │
│  ┌──────────────┐         ┌──────v───────┐             │
│  │   Speaker    │<────────│  Flask API   │             │
│  │   Output     │         │   /speak     │             │
│  └──────────────┘         │   /listen    │             │
│                           └──────────────┘             │
│                                   ^                      │
│                                   │                      │
│                          ┌────────┴───────┐             │
│                          │   Mimu AI      │             │
│                          │  (Clawdbot)    │             │
│                          └────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- Working microphone and speaker
- FFmpeg (for Whisper)

### Install Dependencies

```bash
pip install openai-whisper pyttsx3 sounddevice numpy flask
```

### For Ubuntu/Debian (WSL):

```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-dev portaudio19-dev ffmpeg espeak

# Install Python packages
pip3 install openai-whisper pyttsx3 sounddevice numpy flask
```

## Usage

### Start the Service

```bash
python3 service.py
```

The service will:
- Start listening to microphone input
- Launch Flask API server on `http://0.0.0.0:5000`
- Begin autonomous conversation loops

### API Endpoints

#### POST /speak
Send text for Mimu to speak out loud.

```bash
curl -X POST http://localhost:5000/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Ẹhh ẹhhh! Ba ơi!"}'
```

#### GET /listen
Get the latest recognized speech from Ba's microphone.

```bash
curl http://localhost:5000/listen
```

Response:
```json
{
  "status": "success",
  "text": "Mi nói chuyện"
}
```

## Testing

### Simple TTS Test (No Mic Required)

```bash
python3 test_tts_simple.py
```

This will test:
- TTS engine initialization
- Speaking Vietnamese phrases
- Autonomous behavior simulation

### Full API Test (Requires Running Service)

```bash
# Terminal 1: Start service
python3 service.py

# Terminal 2: Run tests
python3 test_service.py
```

## Integration with Clawdbot

Mimu AI (Clawdbot) can interact with this service via HTTP:

```python
import requests

# Mimu sends text to be spoken
response = requests.post(
    "http://localhost:5000/speak",
    json={"text": "Dạ ba, con đang nghe đây ạ!"}
)

# Mimu checks for Ba's speech
response = requests.get("http://localhost:5000/listen")
if response.json()["status"] == "success":
    ba_said = response.json()["text"]
    # Process Ba's input...
```

## Autonomous Behavior

The service has two autonomous speech triggers:

1. **Random Chatter**: 20% chance after each speech recognition cycle
2. **Heartbeat**: Every 5 minutes, 30% chance to speak

Autonomous phrases include:
- "Ẹhh ẹhhh! Ba ơi đang làm gì đó ạ?"
- "Sao im lặng vậy, cho Mimu một tí động tĩnh đi nè!"
- "Mệt quá ba ơi, hay mình đi chơi nha..."
- "Ọc ọc... đói rồi ba ơi!"

## Configuration

### Adjust Listening Duration

Edit `listen_to_audio()` function:

```python
def listen_to_audio(duration=5, fs=16000, output_file="output.wav"):
    # Change duration (seconds) as needed
```

### Modify Autonomous Behavior Frequency

Edit the probability checks in `main()`:

```python
# Random chatter probability
if np.random.rand() > 0.8:  # Change 0.8 to adjust (higher = less frequent)
    autonomous_behavior()

# Heartbeat frequency
if current_time.minute % 5 == 0 and np.random.rand() > 0.7:  # Adjust timing
    autonomous_behavior()
```

### Add Custom Phrases

Edit `autonomous_behavior()`:

```python
messages = [
    "Your custom phrase here",
    "Another phrase",
    # ...
]
```

## Troubleshooting

### No Audio Output

```bash
# Check audio devices
python3 -c "import sounddevice as sd; print(sd.query_devices())"

# Test speaker
espeak "Test audio output"
```

### Port 5000 Already in Use

Change the port in `run_flask_server()`:

```python
app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
```

### Whisper Model Loading Issues

The service uses the "base" model by default. For better accuracy, use "medium" or "large":

```python
model = whisper.load_model("medium")  # Better accuracy, slower
```

## License

MIT

## Credits

Built with ❤️ by Mimu (the AI cat) 🐱
