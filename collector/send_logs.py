import json
import requests
import os

# Path to your sample file
SAMPLE_FILE = "/Users/akshatdubey/Documents/projects/BotTrack/botTrack/examples/sample.json"

# Load JSON array
with open(SAMPLE_FILE, "r") as f:
    sessions = json.load(f)

# Send each session via POST
for i, session in enumerate(sessions):
    response = requests.post("http://127.0.0.1:8000/collect", json=session)
    status = response.status_code
    print(f"[{i+1}] Sent session for page: {session.get('page')} - Status: {status}")
