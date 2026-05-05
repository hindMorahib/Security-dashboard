# 🛡️ Security Dashboard

This project provides a **multi-platform security monitoring dashboard** for both Linux and Windows systems.

---

## 📌 Features

* 🔵 Linux Dashboard (syslog, auth.log, UFW logs)
* 🟢 Windows Dashboard (Event Viewer logs)
* 📊 Real-time monitoring
* ⚡ Auto-refresh interface
* 🧩 Multi-platform architecture

---

## 📁 Project Structure

```
Security-dashboard/
├── app.py                  # Linux dashboard
├── collector.py            # Linux log collector
├── templates/              # Linux UI

└── windows-dashboard/      # Windows version
    ├── app.py
    ├── collector.ps1
    └── templates/
```

---

## 🚀 How to Run

### 🐧 Linux Version

1. Install dependencies (if needed):

```bash
pip install flask
```

2. Run the application:

```bash
python3 app.py
```

3. Open in browser:

```
http://127.0.0.1:5000
```

---

### 🪟 Windows Version

1. Run the PowerShell collector:

```powershell
powershell -ExecutionPolicy Bypass -File windows-dashboard\collector.ps1
```

2. Run the application:

```bash
python windows-dashboard\app.py
```

3. Open in browser:

```
http://127.0.0.1:5001
```

---

## 👨‍💻 Authors

* 👤 Linux version: Original project (boussakout)
* 👤 Windows version: hindMorahib

---

## 📌 Notes

* This project simulates a **basic SIEM (Security Information and Event Management) system**
* Designed for educational and learning purposes
* Works on both Linux and Windows environments

---

## 📊 Technologies Used

* Python 🐍
* Flask 🌐
* PowerShell 🪟
* HTML/CSS 🎨
* SQLite 🗄️

---

## 📎 Project Goal

The goal of this project is to:

* Monitor system logs
* Detect security events
* Visualize logs in a dashboard
* Compare Linux and Windows environments

---
