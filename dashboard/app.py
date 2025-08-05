import streamlit as st
import json
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scoring.evaluator import evaluate_session
from collections import defaultdict
from datetime import datetime

st.set_page_config(page_title="BotTrack Daily Analytics", layout="wide")
st.title("📊 BotTrack – Daily AI Bot Analytics")

LOG_FILE = "logs/logs.jsonl"

# Load logs
sessions = []
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                session = json.loads(line.strip())
                session["result"] = evaluate_session(session)
                sessions.append(session)
            except:
                continue

if not sessions:
    st.warning("No session logs found. Please use the SDK and collector.")
    st.stop()

# Group by date and page
daily_stats = defaultdict(lambda: defaultdict(lambda: {"success": 0, "failure": 0, "sessions": []}))
for session in sessions:
    date = session.get("date", "unknown")
    page = session.get("page", "unknown")
    result = session["result"]
    daily_stats[date][page][result] += 1
    daily_stats[date][page]["sessions"].append(session)

# Select date
all_dates = sorted(daily_stats.keys())
selected_date = st.selectbox("📅 Select a Date", all_dates[::-1])

# Summary per page
st.subheader(f"📋 Page-wise Summary for {selected_date}")
summary_data = []
for page, stats in daily_stats[selected_date].items():
    total = stats["success"] + stats["failure"]
    fail_pct = (stats["failure"] / total) * 100 if total > 0 else 0
    summary_data.append({
        "Page": page,
        "Sessions": total,
        "Success": stats["success"],
        "Failure": stats["failure"],
        "Failure %": f"{fail_pct:.1f}%"
    })
st.dataframe(summary_data, use_container_width=True)

# Session Viewer
st.subheader("🔍 Sessions on Selected Date and Page")
selected_page = st.selectbox("Select Page", list(daily_stats[selected_date].keys()))

for session in daily_stats[selected_date][selected_page]["sessions"]:
    st.markdown(f"**Result:** :{'green' if session['result']=='success' else 'red'}[{session['result'].upper()}]")
    st.markdown(f"**Start:** {session.get('started_at')} | **End:** {session.get('exited_at')}")
    for msg in session.get("messages", []):
        if msg["sender"] == "user":
            st.markdown(f"🧑‍💬 **User:** {msg['message']}")
        else:
            st.markdown(f"🤖 **Bot:** {msg['message']}")
    st.markdown("---")
