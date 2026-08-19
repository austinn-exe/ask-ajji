import requests
from getpass import getpass

BASE_URL = "http://127.0.0.1:8000"
AUDIO_FILE = "audio.mp4"

print("=== ASK AJJI AI TEST ===")

email = input("Enter your Ask Ajji email: ")
password = getpass("Enter your Ask Ajji password: ")

print("\nLogging in...")

login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    data={
        "username": email,
        "password": password,
        "grant_type": "password"
    }
)

print("Login status:", login_response.status_code)

if login_response.status_code != 200:
    print("LOGIN FAILED")
    print(login_response.text)
    raise SystemExit

token = login_response.json()["access_token"]

print("Login successful!")
print("\nSending audio to Ask Ajji...")
print("Gemini processing may take a little time...")

with open(AUDIO_FILE, "rb") as audio:
    response = requests.post(
        f"{BASE_URL}/api/stories",
        headers={
            "Authorization": f"Bearer {token}"
        },
        data={
            "title": "Ajji Test Memory",
            "contributor_name": "Ajji"
        },
        files={
            "audio": ("audio.mp4", audio, "video/mp4")
        },
        timeout=120
    )

print("\nStory response status:", response.status_code)
print("\n========== RESULT ==========")
print(response.text)
print("============================")