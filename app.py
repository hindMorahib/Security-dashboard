<<<<<<< HEAD

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
=======
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask, jsonify, render_template
from db import init_db, get_events, get_stats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events')
def api_events():
    events = get_events(limit=100)
    result = []
    for row in events:
        result.append({
            "timestamp": row[0],
            "source":    row[1],
            "level":     row[2],
            "message":   row[3]
        })
    return jsonify(result)

@app.route('/api/stats')
def api_stats():
    stats = get_stats()
    result = {
        "CRITICAL": 0,
        "WARNING":  0,
        "INFO":     0
    }
    for row in stats:
        level = row[0]
        count = row[1]
        if level in result:
            result[level] = count
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    print("🌐 Dashboard running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> f27af43a2862f11f436edb6098b25e14413b2cc4
