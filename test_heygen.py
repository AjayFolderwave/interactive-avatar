import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HEYGEN_API_KEY")
avatar_id = os.getenv("HEYGEN_AVATAR_ID")

print(f"API Key: {api_key[:20]}...")
print(f"Avatar ID: {avatar_id}")

# Test 1: List avatars
print("\n📋 Testing avatar list...")
headers = {"X-Api-Key": api_key}
response = requests.get("https://api.heygen.com/v2/avatars", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

# Test 2: Check specific avatar
print("\n🎭 Testing specific avatar...")
response = requests.get(f"https://api.heygen.com/v2/avatars/{avatar_id}", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")