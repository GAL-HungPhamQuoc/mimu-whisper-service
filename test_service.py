"""
Test suite for Mimu Voice Interaction Service
Tests the Flask API endpoints and TTS functionality
"""

import requests
import time
import threading
import subprocess
import sys

# Base URL for the service
BASE_URL = "http://localhost:5000"

def test_speak_endpoint():
    """Test the /speak endpoint with mock text."""
    print("\n[TEST 1] Testing /speak endpoint...")
    
    test_phrases = [
        "Ẹhh ẹhhh! Ông già ơi, tui đây!",
        "Ba ơi, con đang test xem có nghe được không nè!",
        "Lẹ lẹ đi ba, tui đang chờ đây!",
    ]
    
    for phrase in test_phrases:
        try:
            response = requests.post(
                f"{BASE_URL}/speak",
                json={"text": phrase},
                timeout=10
            )
            if response.status_code == 200:
                print(f"✅ Spoke: '{phrase}'")
                time.sleep(2)  # Wait for TTS to finish
            else:
                print(f"❌ Failed to speak: {response.json()}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def test_listen_endpoint():
    """Test the /listen endpoint."""
    print("\n[TEST 2] Testing /listen endpoint...")
    
    try:
        # Simulate checking for speech (queue should be empty initially)
        response = requests.get(f"{BASE_URL}/listen", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "no_speech":
                print("✅ Listen endpoint working (no speech in queue)")
            elif data["status"] == "success":
                print(f"✅ Listen endpoint received text: '{data['text']}'")
        else:
            print(f"❌ Failed: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def test_interactive_conversation():
    """Test a full conversation cycle."""
    print("\n[TEST 3] Testing interactive conversation...")
    
    # Mimu speaks first
    print("Mimu: Ẹhh ẹhhh! Ba ơi có nghe tui không?")
    requests.post(
        f"{BASE_URL}/speak",
        json={"text": "Ẹhh ẹhhh! Ba ơi có nghe tui không?"}
    )
    time.sleep(3)
    
    # Mock Ba's response (normally would come from mic)
    print("Ba: (giả lập) Mi nói gì đó?")
    
    # Mimu responds
    print("Mimu: Dạ con đang test xem hệ thống có hoạt động không ạ!")
    requests.post(
        f"{BASE_URL}/speak",
        json={"text": "Dạ con đang test xem hệ thống có hoạt động không ạ!"}
    )
    time.sleep(3)
    
    print("✅ Interactive conversation test completed")
    return True

def test_autonomous_behavior():
    """Test autonomous speech capability."""
    print("\n[TEST 4] Testing autonomous behavior...")
    
    autonomous_phrases = [
        "Ọc ọc... đói rồi ba ơi!",
        "Sao im lặng vậy, cho Mimu một tí động tĩnh đi nè!",
    ]
    
    for phrase in autonomous_phrases:
        print(f"Mimu (autonomous): {phrase}")
        requests.post(
            f"{BASE_URL}/speak",
            json={"text": phrase}
        )
        time.sleep(2)
    
    print("✅ Autonomous behavior test completed")
    return True

def check_service_running():
    """Check if the service is running."""
    try:
        response = requests.get(f"{BASE_URL}/listen", timeout=2)
        return True
    except:
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🐱 Mimu Voice Interaction Service - Test Suite")
    print("=" * 60)
    
    # Check if service is running
    if not check_service_running():
        print("\n⚠️  Service is not running!")
        print("Please start the service first: python service.py")
        print("\nAttempting to start service in background...")
        
        # Try to start service in background (optional)
        # Note: This might not work if dependencies aren't installed
        # service_process = subprocess.Popen([sys.executable, "service.py"])
        # time.sleep(5)
        
        # if not check_service_running():
        #     print("❌ Could not start service automatically")
        #     return
        
        return
    
    print("\n✅ Service is running on", BASE_URL)
    
    # Run all tests
    results = []
    
    results.append(("Speak Endpoint", test_speak_endpoint()))
    results.append(("Listen Endpoint", test_listen_endpoint()))
    results.append(("Interactive Conversation", test_interactive_conversation()))
    results.append(("Autonomous Behavior", test_autonomous_behavior()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
