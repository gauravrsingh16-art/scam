"""
Database and Classification History Module
Manages SQLite storage for predictions, analytics, and privacy settings.
"""

import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
from config import HISTORY_DB_PATH


def get_connection() -> sqlite3.Connection:
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(HISTORY_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables and default settings if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Classification History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            message_type TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            char_count INTEGER NOT NULL,
            vectorizer_used TEXT NOT NULL,
            text_preview TEXT DEFAULT ''
        )
    """)

    # Privacy and System Settings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Default settings: History enabled (1), Store Message Previews disabled (0)
    cursor.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('history_enabled', '1')")
    cursor.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('store_previews', '0')")

    conn.commit()
    conn.close()


def is_history_enabled() -> bool:
    """Check if classification logging is currently enabled."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM app_settings WHERE key = 'history_enabled'")
    row = cursor.fetchone()
    conn.close()
    return bool(int(row["value"])) if row else True


def set_history_enabled(enabled: bool) -> None:
    """Enable or disable classification logging."""
    conn = get_connection()
    cursor = conn.cursor()
    val = "1" if enabled else "0"
    cursor.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES ('history_enabled', ?)", (val,))
    conn.commit()
    conn.close()


def is_preview_storage_enabled() -> bool:
    """Check if storing message preview is allowed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM app_settings WHERE key = 'store_previews'")
    row = cursor.fetchone()
    conn.close()
    return bool(int(row["value"])) if row else False


def set_preview_storage_enabled(enabled: bool) -> None:
    """Enable or disable storing sanitized message previews."""
    conn = get_connection()
    cursor = conn.cursor()
    val = "1" if enabled else "0"
    cursor.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES ('store_previews', ?)", (val,))
    conn.commit()
    conn.close()


def log_classification(
    message_type: str,
    prediction: str,
    confidence: float,
    char_count: int,
    vectorizer_used: str = "tfidf",
    text: Optional[str] = None
) -> bool:
    """
    Log a classification event to SQLite.
    Adheres strictly to user privacy preferences.
    """
    if not is_history_enabled():
        return False

    preview = ""
    if is_preview_storage_enabled() and text:
        # Sanitize and truncate to first 60 chars
        clean_snip = " ".join(text.split())[:60]
        preview = clean_snip + ("..." if len(text) > 60 else "")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO classification_history
        (timestamp, message_type, prediction, confidence, char_count, vectorizer_used, text_preview)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        message_type,
        prediction.upper(),
        round(float(confidence), 4),
        int(char_count),
        vectorizer_used,
        preview
    ))
    conn.commit()
    conn.close()
    return True


def get_history(limit: int = 100) -> pd.DataFrame:
    """Retrieve recent classification history as a pandas DataFrame."""
    conn = get_connection()
    query = """
        SELECT id, timestamp, message_type, prediction, confidence, char_count, vectorizer_used, text_preview
        FROM classification_history
        ORDER BY id DESC
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df


def get_dashboard_stats() -> Dict[str, Any]:
    """Calculate real-time metrics and summary analytics from actual history."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM classification_history")
    total = cursor.fetchone()["total"]

    if total == 0:
        conn.close()
        return {
            "total_processed": 0,
            "total_spam": 0,
            "total_ham": 0,
            "spam_rate": 0.0,
            "avg_confidence": 0.0,
            "sms_count": 0,
            "email_count": 0,
            "bulk_count": 0,
            "has_records": False,
        }

    cursor.execute("SELECT COUNT(*) AS spam_count FROM classification_history WHERE prediction = 'SPAM'")
    spam_count = cursor.fetchone()["spam_count"]
    ham_count = total - spam_count
    spam_rate = round((spam_count / total) * 100, 2)

    cursor.execute("SELECT AVG(confidence) AS avg_conf FROM classification_history")
    avg_conf = cursor.fetchone()["avg_conf"]
    avg_conf_pct = round((avg_conf or 0.0) * 100, 2)

    cursor.execute("SELECT COUNT(*) AS cnt FROM classification_history WHERE message_type = 'SMS'")
    sms_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM classification_history WHERE message_type = 'Email'")
    email_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM classification_history WHERE message_type = 'Bulk'")
    bulk_count = cursor.fetchone()["cnt"]

    conn.close()

    return {
        "total_processed": total,
        "total_spam": spam_count,
        "total_ham": ham_count,
        "spam_rate": spam_rate,
        "avg_confidence": avg_conf_pct,
        "sms_count": sms_count,
        "email_count": email_count,
        "bulk_count": bulk_count,
        "has_records": True,
    }


def clear_history() -> int:
    """Clear all records from classification history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classification_history")
    deleted = cursor.rowcount
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='classification_history'")
    conn.commit()
    conn.close()
    return deleted


def delete_history_record(record_id: int) -> bool:
    """Delete a single classification record by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classification_history WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_history_filtered(
    search_query: str = "",
    category_filter: str = "ALL",
    message_type_filter: str = "ALL",
    limit: int = 500
) -> pd.DataFrame:
    """Retrieve filtered history records based on search keywords and filter criteria."""
    conn = get_connection()
    conditions = []
    params = []

    if search_query.strip():
        term = f"%{search_query.strip()}%"
        conditions.append("(text_preview LIKE ? OR id LIKE ? OR prediction LIKE ?)")
        params.extend([term, term, term])

    if category_filter.upper() in ["SPAM", "HAM", "NOT SPAM"]:
        cat = "SPAM" if category_filter.upper() == "SPAM" else "NOT SPAM"
        conditions.append("prediction = ?")
        params.append(cat)

    if message_type_filter.upper() in ["SMS", "EMAIL", "BULK"]:
        conditions.append("UPPER(message_type) = ?")
        params.append(message_type_filter.upper())

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"""
        SELECT id, timestamp, message_type, prediction, confidence, char_count, vectorizer_used, text_preview
        FROM classification_history
        {where_clause}
        ORDER BY id DESC
        LIMIT ?
    """
    params.append(limit)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_db_file_size() -> str:
    """Get the physical file size of the SQLite database in human-readable format."""
    import os
    if not HISTORY_DB_PATH.exists():
        return "0 KB"
    size_bytes = os.path.getsize(HISTORY_DB_PATH)
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def reindex_database() -> bool:
    """Optimize SQLite database via VACUUM and ANALYZE."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("VACUUM")
    cursor.execute("ANALYZE")
    conn.commit()
    conn.close()
    return True

