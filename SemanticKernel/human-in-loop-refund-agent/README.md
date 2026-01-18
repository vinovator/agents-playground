# 💸 Human-in-the-Loop (HITL) Refund Agent

A robust demonstration of building **Stateful AI Agents** using **Semantic Kernel** and **Google Gemini**.

This project simulates a real-world refund processing system where an AI agent handles customer requests autonomously but intelligently pauses execution to seek human approval for high-risk transactions.

## 📋 Scenario & Logic

The agent follows a strict business policy defined in `config.py`:

* **🟢 Low Value (< $50):** The agent automatically approves the refund and updates the database instantly.
* **🔴 High Value (≥ $50):** The agent recognizes the risk, creates a ticket in the database with a status of `PENDING_APPROVAL`, and informs the user that a manager must review it.
* **🛡️ Manager Dashboard:** A separate UI view allows a human to review, approve, or reject these pending requests.

## 🛠️ Tech Stack

* **Orchestration:** [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) (Python)
* **LLM:** Google Gemini 2.5 Flash
* **Interface:** [Streamlit](https://streamlit.io/) (Chat UI + Admin Dashboard)
* **Persistence:** SQLite (File-based SQL database)
* **Language:** Python 3.10+

## 📂 Project Structure

This project follows a modular architecture to separate concerns between the UI, the AI Logic, and the Data Layer.

```text
human-in-loop-refund-agent/
├── app.py                 # 🖥️ The Entry Point (Streamlit UI)
├── agent.py               # 🧠 The AI Brain (Semantic Kernel Setup)
├── database.py            # 💾 The Persistence Layer (SQLite Operations)
├── config.py              # ⚙️ Configuration & Business Constants
├── .env                   # 🔐 Secrets (API Keys - Not committed to git)
├── requirements.txt       # 📦 Dependencies
└── plugins/               # 🔌 AI Skills/Tools
    └── refund_plugin.py   #    - Logic for processing refunds

```

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10 or higher installed.
* A Google Cloud API Key for Gemini (Get one [here](https://aistudio.google.com/)).

### 2. Installation

1. **Clone the repository** (or create the folder):
```bash
mkdir refund_agent
cd "human-in-loop-refund-agent"
```


2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```


3. **Configure Environment**:
Create a file named `.env` in the root folder and add your API key:
```ini
GOOGLE_API_KEY=your_actual_api_key_here
```



### 3. Running the Application

Run the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## 🎮 How to Use

### Scene 1: The Auto-Approval

1. In the **Customer Chat** (left column), type:
> "I need a refund of $20 for a broken toaster."


2. **Observation:** The agent checks the limit ($20 < $50), auto-approves it, and you will see a success message.

### Scene 2: The Human-in-the-Loop

1. In the **Customer Chat**, type:
> "I need a refund of $150 because the TV never arrived."


2. **Observation:** The agent sees the amount ($150 > $50). It will **stop** and tell you: *"Approval Required... A manager has been notified."*
3. Look at the **Manager Dashboard** (right column). You will see a new "Pending Request" appear.
4. Click **✅ Approve**. The status in the database updates, and the flow is complete.

## ⚙️ Configuration

You can modify the business rules without touching the code logic. Open `config.py`:

```python
# Change the approval threshold
REFUND_AUTO_APPROVE_LIMIT = 100.0 

# Change the currency symbol
CURRENCY_SYMBOL = "€"
```

## 🧠 Key Concepts Learned

This project demonstrates:

* **Plugin Architecture:** Encapsulating logic in `plugins/refund_plugin.py` so the LLM uses it as a tool.
* **State Persistence:** Using SQLite to bridge the gap between an AI conversation and a Human action that might happen hours later.
* **Framework Separation:** Keeping the AI code (`agent.py`) separate from the UI code (`app.py`).