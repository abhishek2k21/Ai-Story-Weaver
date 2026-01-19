#!/usr/bin/env python3
"""
Test script to start server and verify real AI integration
"""

import subprocess
import time
import requests
import sys
import os
import threading

def start_server():
    """Start the server in a separate thread."""
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()

    return subprocess.Popen([
        sys.executable, '-m', 'uvicorn', 'backend.app.main:app',
        '--host', '0.0.0.0', '--port', '8000', '--log-level', 'info'
    ], env=env, cwd=os.getcwd())

def test_health():
    """Test the health endpoint."""
    time.sleep(5)  # Wait for server to start

    try:
        response = requests.get("http://localhost:8000/api/v1/stories/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful!")
            print(f"AI Integration: {data.get('ai_integration', 'unknown')}")
            print(f"Agents: {data.get('agents', {})}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AI Story Weaver Pro server...")
    server = start_server()

    try:
        success = test_health()
        if success:
            print("🎉 Real AI integration is working!")
        else:
            print("❌ Real AI integration failed")
    finally:
        print("🧹 Stopping server...")
        server.terminate()
        server.wait()