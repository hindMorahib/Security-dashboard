import sqlite3

DB_NAME = "dashboard.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        source TEXT,
        level TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_event(time, source, level, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs (time, source, level, message)
    VALUES (?, ?, ?, ?)
    """, (time, source, level, message))

    conn.commit()
    conn.close()

def get_events(limit=100):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT time, source, level, message
    FROM logs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT level, COUNT(*)
    FROM logs
    GROUP BY level
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows