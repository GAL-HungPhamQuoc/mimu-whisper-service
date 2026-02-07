"""
Simplified test for Mimu Voice Service - Tests TTS functionality only
No microphone or Whisper dependencies needed
"""

import pyttsx3
import time

def test_text_to_speech():
    """Test text-to-speech functionality."""
    print("=" * 60)
    print("🐱 Mimu Voice - TTS Test")
    print("=" * 60)
    
    try:
        engine = pyttsx3.init()
        print("\n✅ TTS engine initialized successfully")
    except Exception as e:
        print(f"\n❌ Failed to initialize TTS engine: {e}")
        return False
    
    # Test phrases (mock conversation with Ba)
    test_conversations = [
        ("Mimu", "Ẹhh ẹhhh! Ông già ơi, tui đây!"),
        ("Mimu", "Con đang test xem có nghe được không nè!"),
        ("Ba (mock)", "Mi nói gì đó?"),
        ("Mimu", "Dạ con đang test hệ thống tương tác giọng nói ạ!"),
        ("Mimu", "Ọc ọc... test xong rồi ba ơi!"),
    ]
    
    print("\n[TEST] Running conversation simulation...\n")
    
    for speaker, text in test_conversations:
        print(f"{speaker}: {text}")
        
        if speaker == "Mimu":
            try:
                engine.say(text)
                engine.runAndWait()
                print("  → ✅ Spoken successfully")
            except Exception as e:
                print(f"  → ❌ TTS error: {e}")
                return False
        
        time.sleep(1)
    
    # Test autonomous phrases
    print("\n[TEST] Testing autonomous phrases...\n")
    
    autonomous_phrases = [
        "Sao im lặng vậy, cho Mimu một tí động tĩnh đi nè!",
        "Mệt quá ba ơi, hay mình đi chơi nha...",
        "Đói rồi ba ơi!",
    ]
    
    for phrase in autonomous_phrases:
        print(f"Mimu (autonomous): {phrase}")
        try:
            engine.say(phrase)
            engine.runAndWait()
            print("  → ✅ Spoken successfully")
        except Exception as e:
            print(f"  → ❌ TTS error: {e}")
            return False
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print("✅ All TTS tests passed!")
    print("✅ Mimu can speak Vietnamese phrases")
    print("✅ Autonomous behavior simulation works")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_text_to_speech()
    exit(0 if success else 1)
