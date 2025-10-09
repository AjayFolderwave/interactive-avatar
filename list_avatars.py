import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HEYGEN_API_KEY")

headers = {
    "X-Api-Key": api_key
}

# Try to list avatars
url = "https://api.heygen.com/v2/avatars"

response = requests.get(url, headers=headers)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    if "data" in data and "avatars" in data["data"]:
        print("\n📋 YOUR AVATARS:")
        for avatar in data["data"]["avatars"]:
            print(f"\nName: {avatar.get('avatar_name', 'N/A')}")
            print(f"ID: {avatar.get('avatar_id', 'N/A')}")
            print(f"Type: {avatar.get('avatar_type', 'N/A')}")