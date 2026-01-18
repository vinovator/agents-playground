import streamlit as st
import asyncio
import pandas as pd
from semantic_kernel.contents import ChatHistory

# --- Local Imports (Refactored Structure) ---
import database
import config
from agent import get_response_from_agent

# --- Page Configuration ---
st.set_page_config(
    page_title="Human-in-The-Loop Refund Agent", 
    layout="wide",
    page_icon="💸"
)
st.title("💸 AI Refund Agent (Human-in-the-Loop)")

# --- Initialization ---

# 1. Initialize Database on first run
if "db_init" not in st.session_state:
    database.init_db()
    st.session_state.db_init = True

# 2. Initialize Chat History for Semantic Kernel
if "history" not in st.session_state:
    st.session_state.history = ChatHistory()
    # System prompt to guide behavior
    st.session_state.history.add_system_message(
        "You are a helpful customer service agent. You can process refunds. "
        "Always ask for the reason and the amount if not provided."
    )

# 3. Initialize Message Log for UI rendering
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LAYOUT ---
col_chat, col_admin = st.columns([1, 1], gap="large")

# ==========================================
# COLUMN 1: CUSTOMER CHAT INTERFACE
# ==========================================
with col_chat:
    st.subheader("💬 Customer Chat")
    st.info(f"ℹ️ Auto-approval limit: {config.CURRENCY_SYMBOL}{config.REFUND_AUTO_APPROVE_LIMIT}")

    # Container for chat messages
    chat_container = st.container(height=500)
    
    # Display Chat History
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("I need a refund..."):
        # 1. Render User Message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # 2. Get Agent Response (Async call to agent.py)
        with st.spinner("Agent is thinking..."):
            response_text = asyncio.run(
                get_response_from_agent(prompt, st.session_state.history)
            )

        # 3. Render Agent Message
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response_text)
        
        # 4. Trigger UI update to refresh the Admin Panel immediately
        st.rerun()

# ==========================================
# COLUMN 2: MANAGER APPROVAL DASHBOARD
# ==========================================
with col_admin:
    st.subheader("🛡️ Manager Dashboard")
    st.caption("Requests exceeding the threshold require manual review.")
    
    st.divider()
    
    # Fetch Pending Requests from Database
    pending_df = database.get_pending_approvals()
    
    if pending_df.empty:
        st.success("✅ All clear! No pending approvals.")
    else:
        st.warning(f"⚠️ {len(pending_df)} Request(s) Pending Action")
        
        # Iterate through pending requests
        for index, row in pending_df.iterrows():
            # Create a card-like container for each request
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                
                with c1:
                    st.markdown(f"**Ticket #{row['id']}**")
                    st.markdown(f"**Reason:** {row['reason']}")
                    st.caption(f"User: {row['user_id']} | Time: {row['timestamp']}")
                
                with c2:
                    st.metric(label="Amount", value=f"{config.CURRENCY_SYMBOL}{row['amount']}")

                # Action Buttons
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button("✅ Approve", key=f"app_{row['id']}", use_container_width=True):
                        database.update_refund_status(row['id'], "APPROVED")
                        st.toast(f"Ticket #{row['id']} Approved!")
                        st.rerun()
                
                with b_col2:
                    if st.button("❌ Reject", key=f"rej_{row['id']}", use_container_width=True):
                        database.update_refund_status(row['id'], "REJECTED")
                        st.toast(f"Ticket #{row['id']} Rejected!")
                        st.rerun()

    # --- Debug View (Optional) ---
    with st.expander("🔍 View All Database Records"):
        import sqlite3
        conn = sqlite3.connect(database.DB_FILE)
        all_data = pd.read_sql_query("SELECT * FROM refund_requests ORDER BY id DESC", conn)
        st.dataframe(all_data, use_container_width=True)
        conn.close()