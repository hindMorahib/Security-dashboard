
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect("dashboard.db")
    cursor = conn.cursor()

    cursor.execute("SELECT level, message FROM logs ORDER BY id DESC LIMIT 100")
    logs = cursor.fetchall()

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