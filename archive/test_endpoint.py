#!/usr/bin/env python3
import requests
import json

def test_backend():
    base_url = "http://localhost:8001"
    
    print("Testing backend endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test chat endpoint
    try:
        chat_data = {
            "message": "Hello, test message",
            "role": "client",
            "session_id": "test_session_123"
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        print(f"Chat endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Chat endpoint failed: {e}")
    
    # Test conversations endpoint
    try:
        response = requests.get(f"{base_url}/conversations/test_session_123")
        print(f"Conversations endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Conversations endpoint failed: {e}")

if __name__ == "__main__":
    test_backend()
