import sqlite3
from datetime import datetime
import pandas as pd

# Database setup
DB_FILE = "refunds.db"

def init_db():
    """
    Initializes the SQLite database with a refunds table
    """

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refund_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        reason TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL, -- 'APPROVED', 'REJECTED', 'PENDING APPROVAL'
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# CRUD Operations

def create_refund_request(user_id: str, reason: str, amount: float, status: str) -> int:
    """
    Creates a new refund request
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO refund_requests (user_id, reason, amount, status)
    VALUES (?, ?, ?, ?)
    """, (user_id, reason, amount, status)
    )

    conn.commit()
    conn.close()

def get_pending_approvals():
    """
    Retrieves all refund requests that are pending approval
    """
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM refund_requests WHERE status = 'PENDING APPROVAL'", conn)
    conn.close()
    return df

def update_refund_status(request_id: int, new_status: str):
    """
    Updates the status of a refund request
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE refund_requests SET status = ? WHERE id = ?
    """, (new_status, request_id)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")