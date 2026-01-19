#!/usr/bin/env python3
"""
AI Agent Integration Setup Script for AI Story Weaver Pro

This script helps configure real API keys for AI agent integration.
Run this script to set up real AI agents instead of mock responses.
"""

import os
import sys
from pathlib import Path

def setup_ai_integration():
    """Guide user through AI integration setup."""
    print("🤖 AI Story Weaver Pro - AI Agent Integration Setup")
    print("=" * 60)

    env_file = Path(".env")

    if not env_file.exists():
        print("❌ .env file not found. Please run setup from the project root directory.")
        return False

    print("Current API key status:")
    print("-" * 30)

    # Read current .env file
    env_content = {}
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                env_content[key] = value

    # Check API key status
    api_keys = {
        'OPENAI_API_KEY': 'OpenAI GPT-4 (Primary AI agent)',
        'ANTHROPIC_API_KEY': 'Anthropic Claude (Alternative AI agent)',
        'HUGGINGFACE_API_KEY': 'Hugging Face (Optional embeddings)',
        'ELEVENLABS_API_KEY': 'ElevenLabs (Text-to-speech)',
    }

    configured_keys = []
    for key, description in api_keys.items():
        value = env_content.get(key, '')
        if value and not value.startswith('your-') and len(value) > 20:
            print(f"✅ {key}: Configured ({description})")
            configured_keys.append(key)
        else:
            print(f"❌ {key}: Not configured ({description})")

    print("\n" + "=" * 60)

    if configured_keys:
        print(f"🎉 {len(configured_keys)} API key(s) are configured!")
        print("Real AI agents will be used for story generation.")
        return True
    else:
        print("⚠️  No real API keys configured.")
        print("The system will use mock responses for testing.")
        print("\nTo enable real AI integration:")
        print("1. Get API keys from the respective services:")
        print("   - OpenAI: https://platform.openai.com/api-keys")
        print("   - Anthropic: https://console.anthropic.com/")
        print("   - Hugging Face: https://huggingface.co/settings/tokens")
        print("   - ElevenLabs: https://elevenlabs.io/app/profile")
        print("\n2. Update the .env file with your real API keys")
        print("3. Restart the backend server")
        print("\nExample .env configuration:")
        print("OPENAI_API_KEY=sk-your-actual-openai-key-here")
        print("ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here")

        return False

def test_ai_integration():
    """Test if AI integration is working."""
    print("\n🧪 Testing AI Integration")
    print("-" * 30)

    try:
        import requests

        # Test health endpoint
        response = requests.get("http://localhost:8000/api/v1/stories/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            ai_status = data.get('ai_integration', 'unknown')

            if ai_status == 'enabled':
                print("✅ AI integration is ENABLED")
                print("Real AI agents are active for story generation")
            else:
                print("⚠️  AI integration is DISABLED")
                print("Using mock responses for testing")
                print("Configure API keys to enable real AI agents")

            print(f"Agent status: {data.get('agents', {})}")
            return True
        else:
            print("❌ Health check failed")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend server: {e}")
        print("Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Change to project root if running from scripts directory
    if Path(__file__).parent.name == 'scripts':
        os.chdir(Path(__file__).parent.parent)

    success = setup_ai_integration()
    test_ai_integration()

    print("\n" + "=" * 60)
    if success:
        print("🎉 AI integration setup complete!")
        print("Your AI Story Weaver Pro is ready with real AI agents.")
    else:
        print("📝 Setup complete with mock responses.")
        print("Configure API keys when ready for real AI integration.")

    print("\nTo restart with new configuration:")
    print("1. Stop the backend server (Ctrl+C)")
    print("2. Start the backend server again")
    print("3. Test story generation in the frontend")