import sqlite3
import os
import pandas as pd
from datetime import datetime

# Define database path relative to this file
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'journal.db')

def get_connection():
    """Ensure directory exists and return SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize database and create tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            entry TEXT NOT NULL,
            analysis TEXT NOT NULL,
            mood_score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(entry_text: str, analysis_text: str, mood_score: int):
    """Insert a new journal entry into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO entries (date, entry, analysis, mood_score)
        VALUES (?, ?, ?, ?)
    ''', (date_str, entry_text, analysis_text, mood_score))
    conn.commit()
    conn.close()

def get_all_entries() -> pd.DataFrame:
    """Fetch all entries sorted by date descending."""
    conn = get_connection()
    query = "SELECT * FROM entries ORDER BY date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_recent_entries(days: int = 7) -> pd.DataFrame:
    """Fetch entries from the last n days."""
    conn = get_connection()
    # Calculate threshold date in Python
    threshold_date = (datetime.now() - pd.Timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    
    query = "SELECT * FROM entries WHERE date >= ? ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=(threshold_date,))
    conn.close()
    return df
