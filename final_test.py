#!/usr/bin/env python3
"""
Simple test to verify real AI integration
"""

import os
import sys
import time
import requests
import subprocess
import threading

def test_ai_integration():
    """Test that real AI agents are working."""
    print("🧪 Testing Real AI Integration")
    print("=" * 50)

    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = 'backend'

    # Start server
    print("🚀 Starting server...")
    server = subprocess.Popen([
        sys.executable, 'debug_server.py'
    ], env=env, cwd=os.getcwd())

    try:
        # Wait for server
        print("⏳ Waiting for server to start...")
        time.sleep(8)

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
            print(f"❌ Health check failed: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False
    finally:
        # Clean up
        print("🧹 Stopping server...")
        server.terminate()
        server.wait()

if __name__ == "__main__":
    success = test_ai_integration()

    print("\n" + "=" * 50)
    if success:
        print("🎉 Real AI integration test PASSED!")
        print("Your therapeutic AI storytelling platform is ready!")
    else:
        print("❌ Real AI integration test FAILED!")
        print("Check your configuration.")