import streamlit as st
import json
import os
from scoring.evaluator import evaluate_session
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="BotTrack Session Scorer", layout="wide")
st.title("🧪 BotTrack Session Scorer")

# Log file selection
log_file = st.file_uploader("📄 Upload a BotTrack log file (.jsonl)", type=["jsonl"])

if log_file:
    sessions = []
    for line in log_file:
        try:
            session = json.loads(line.decode("utf-8").strip())
            session["result"] = evaluate_session(session)
            sessions.append(session)
        except Exception as e:
            st.warning(f"⚠️ Error parsing session: {e}")

    if not sessions:
        st.warning("No valid sessions found.")
        st.stop()

    # Group sessions by page
    page_sessions = defaultdict(list)
    for s in sessions:
        page_sessions[s.get("page", "unknown")].append(s)

    selected_page = st.selectbox("📍 Select Page", sorted(page_sessions.keys()))

    page_data = page_sessions[selected_page]
    st.markdown(f"### 💬 {len(page_data)} sessions for `{selected_page}`")

    success_count = sum(1 for s in page_data if s["result"] == "success")
    failure_count = sum(1 for s in page_data if s["result"] == "failure")

    st.metric("✅ Success", success_count)
    st.metric("❌ Failure", failure_count)
    st.progress(failure_count / len(page_data) if page_data else 0)

    # Session viewer
    for i, session in enumerate(page_data):
        with st.expander(f"Session {i+1} - {session['result'].upper()}"):
            for msg in session.get("messages", []):
                prefix = "🧑‍💬" if msg["sender"] == "user" else "🤖"
                st.markdown(f"{prefix} **{msg['sender'].capitalize()}:** {msg['message']}")
