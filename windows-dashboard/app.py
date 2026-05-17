from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard.db")

def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT level, time || ' - ' || source || ' - ' || substr(message, 1, 180) || '...' FROM logs ORDER BY id DESC LIMIT 100")
    logs = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='CRITICAL'")
    critical = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='WARNING'")
    warning = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='INFO'")
    info = cursor.fetchone()[0]

    cursor.execute("""
SELECT COUNT(*) FROM logs
WHERE level='CRITICAL'
OR message LIKE '%échec%'
OR message LIKE '%failed%'
OR message LIKE '%login failed%'
""")
    failed_logins = cursor.fetchone()[0]

    conn.close()
    return logs, total, critical, warning, info, failed_logins

@app.route("/")
def index():
    logs, total, critical, warning, info, failed_logins = get_data()
    return render_template(
        "index.html",
        logs=logs,
        total=total,
        critical=critical,
        warning=warning,
        info=info,
        failed_logins=failed_logins
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)