# 🛠️ DETask

This app displays a list of countries and their flags in an interactive dashboard.

---

## 🧰 Requirements

Make sure the following are installed on your system:

- Python 3.8+
- WSL (Windows Subsystem for Linux)
- A Linux distribution (e.g. Ubuntu via WSL)
- Docker Desktop (running and initialized)
- pip (Python package manager)

---

## 🚀 How to Run the App

1. **Download** or clone all project files into a folder (e.g. on your Desktop).

2. **Run the files in the following order**:

   ### 1. Start the PostgreSQL database
   ```bash
   docker-compose up -d
   ```

   This will start a PostgreSQL container using Docker.

   ### 2. Import the data into the database
   ```bash
   python import.py
   ```

   This creates the `countries` table and populates it with country names and flag URLs.

   ### 3. Run the dashboard
   ```bash
   python viz.py
   ```

   This starts a Dash web application.

   ### 4. Open the app in your browser

   After starting the dashboard, hold **Ctrl** and click the IP address shown in the terminal (typically `http://127.0.0.1:8050`) to open the dashboard in your browser.

---

## ✅ Features

- Scrollable, sortable table of countries
- Click a country row to display its flag
- Interactive and lightweight UI

---

## 📄 Notes

- The database runs in Docker; no external PostgreSQL installation is required.
- You can stop everything using:
  ```bash
  docker-compose down
  ```
