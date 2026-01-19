#!/usr/bin/env python3
"""
Simple test script to verify the story generation API endpoint.
"""

import requests
import json

def test_api():
    """Test the story generation API endpoint."""
    url = "http://localhost:8000/api/v1/stories/test-generate"
    payload = {
        "prompt": "A young person overcoming anxiety through a magical forest journey",
        "therapeutic_focus": "anxiety_management"
    }

    try:
        print("Testing API endpoint:", url)
        print("Payload:", json.dumps(payload, indent=2))

        response = requests.post(url, json=payload, timeout=30)

        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print(f"Story ID: {data.get('story_id')}")
            print(f"Title: {data.get('title')}")
            print(f"Content length: {len(data.get('content', ''))} characters")
            print(f"Created at: {data.get('created_at')}")

            # Show first 200 characters of the story
            content = data.get('content', '')
            print(f"\nStory preview:\n{content[:200]}...")
            return True
        else:
            print("❌ API call failed!")
            print("Response:", response.text)
            return False

    except requests.exceptions.RequestException as e:
        print("❌ Connection error:", str(e))
        return False
    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return False

if __name__ == "__main__":
    print("🧪 Testing AI Story Weaver Pro API")
    print("=" * 50)

    success = test_api()

    print("\n" + "=" * 50)
    if success:
        print("🎉 API test completed successfully!")
        print("The backend is ready for frontend integration.")
    else:
        print("❌ API test failed. Please check the backend server.")