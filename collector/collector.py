from fastapi import FastAPI, Request
import json
from datetime import datetime
import os

app = FastAPI()
LOG_FILE = "logs.jsonl"

# ✅ CORS support added correctly
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:5500"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Log collector endpoint
@app.post("/collect")
async def collect_log(request: Request):
    data = await request.json()
    data["collected_at"] = datetime.utcnow().isoformat()
    data["date"] = datetime.utcnow().strftime("%Y-%m-%d")  # ⬅ Adds daily date

    os.makedirs("logs", exist_ok=True)
    with open(os.path.join("logs", LOG_FILE), "a") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "ok"}
