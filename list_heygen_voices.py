import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HEYGEN_API_KEY")

headers = {"X-Api-Key": api_key}

# List available voices
response = requests.get("https://api.heygen.com/v2/voices", headers=headers)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    voices = data.get("data", {}).get("voices", [])
    
    print(f"\n📋 YOU HAVE {len(voices)} VOICES AVAILABLE:\n")
    
    # Show first 20 voices
    for i, voice in enumerate(voices[:20]):
        print(f"{i+1}. Name: {voice.get('voice_name', 'N/A')}")
        print(f"   ID: {voice.get('voice_id', 'N/A')}")
        print(f"   Gender: {voice.get('gender', 'N/A')}")
        print(f"   Language: {voice.get('language', 'N/A')}\n")
    
    # Look for English male voices
    print("\n🎯 RECOMMENDED VOICES (English Male):")
    for voice in voices:
        if voice.get('gender') == 'male' and 'english' in voice.get('language', '').lower():
            print(f"✅ {voice.get('voice_name')} - ID: {voice.get('voice_id')}")
else:
    print(f"Error: {response.text}")