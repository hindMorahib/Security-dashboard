from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "dashboard.db"

def get_data():
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

    cursor.execute("""
    SELECT time, source, level, message
    FROM logs
    ORDER BY id DESC
    LIMIT 100
    """)
    rows = cursor.fetchall()

    logs = []
    for row in rows:
        time = row[0] or ""
        source = row[1] or ""
        level = row[2] or "INFO"
        message = row[3] or ""

        full_message = f"{time} - {source} - {message}"
        logs.append((level, full_message))

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='CRITICAL'")
    critical = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='WARNING'")
    warning = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='INFO'")
    info = cursor.fetchone()[0]

    conn.close()

    return logs, total, critical, warning, info


@app.route("/")
def index():
    logs, total, critical, warning, info = get_data()

    return render_template(
        "index.html",
        logs=logs,
        total=total,
        critical=critical,
        warning=warning,
        info=info
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    