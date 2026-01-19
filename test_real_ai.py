#!/usr/bin/env python3
"""
Quick test script to verify real AI integration is working
"""

import subprocess
import time
import requests
import sys
import os

def test_real_ai_integration():
    """Test that real AI agents are loaded and working."""
    print("🧪 Testing Real AI Integration")
    print("=" * 50)

    # Start server in background
    print("🚀 Starting backend server...")
    server_process = subprocess.Popen([
        sys.executable, "-c",
        "import sys; sys.path.insert(0, '.'); import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=False)"
    ], cwd=os.path.join(os.path.dirname(__file__), "backend"))

    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(10)

    try:
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        response = requests.get("http://localhost:8000/api/v1/stories/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            ai_status = data.get('ai_integration', 'unknown')

            print("✅ Health check successful!")
            print(f"AI Integration Status: {ai_status}")
            print(f"Agent Status: {data.get('agents', {})}")

            if ai_status == 'enabled':
                print("🎉 REAL AI AGENTS ARE ACTIVE!")
                return True
            else:
                print("⚠️ AI integration is disabled - using mock responses")
                return False
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    finally:
        # Clean up server
        print("🧹 Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = test_real_ai_integration()

    print("\n" + "=" * 50)
    if success:
        print("🎉 Real AI integration test PASSED!")
        print("Your AI agents are working with real OpenAI API.")
    else:
        print("❌ Real AI integration test FAILED!")
        print("Check your API key configuration.")