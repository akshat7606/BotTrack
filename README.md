# 🤖 BotTrack – AI Bot Success & Failure Analytics

**BotTrack** is an open-source analytics toolkit that helps developers and teams measure the performance of their AI bots on every web page — in real time or on a daily basis.

## 🌟 Features

- 📄 Page-level tracking of AI bot sessions
- ✅ Detects success/failure using session rephrases or escalation
- 📊 Streamlit dashboard with date filters and page summaries
- 🧠 Evaluator with intelligent rephrasing detection
- 📦 Works with any LLM bot: Rasa, LangChain, custom, etc.
- 🛠️ Drop-in JavaScript SDK for websites

---

## 🧩 Components

| Folder/File        | Purpose                              |
|--------------------|---------------------------------------|
| `sdk/`             | JavaScript SDK for web tracking       |
| `collector/`       | FastAPI backend for collecting logs   |
| `scoring/`         | Evaluator to classify sessions        |
| `dashboard/`       | Streamlit app with per-page analytics |
| `cli.py`           | Command-line tool for batch scoring   |
| `examples/`        | Sample logs for testing               |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
