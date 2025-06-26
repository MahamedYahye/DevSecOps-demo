
import logging
from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.secret_key = "zeer_zwakke_sleutel"  # Hardcoded credential vulnerability

# Zet debug-logging aan
app.logger.setLevel(logging.DEBUG)

# Registreer de Prometheus-exporter
metrics = PrometheusMetrics(app, path="/metrics")
metrics.info("app_info", "Applicatie metadata", version="1.0.0")

# Hardcoded credentials - vulnerability
# API_KEY = "abcdef1234567890"
# HARDCODED_PASSWORD = "wachtwoord123!"


# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT,
            role TEXT
        )
    """
    )

    # Check if data already exists to avoid duplicates
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]

    if count == 0:
        # Sample data met hardcoded wachtwoord
        c.execute(
            "INSERT INTO users (id, username, password, email, role) VALUES (?, ?, ?, ?, ?)",
            (1, "admin", HARDCODED_PASSWORD, "admin@demo.com", "administrator"),
        )
        c.execute(
            "INSERT INTO users (id, username, password, email, role) VALUES (?, ?, ?, ?, ?)",
            (2, "user", "password123", "user@demo.com", "user"),
        )
        c.execute(
            "INSERT INTO users (id, username, password, email, role) VALUES (?, ?, ?, ?, ?)",
            (3, "guest", "guest", "guest@demo.com", "guest"),
        )

    conn.commit()
    conn.close()


# Home route - Test pagina
@app.route("/")
def home():
    return render_template("Test.html")


@app.route("/Test")
def test_route():
    return render_template("Test.html")


# Kwetsbaarheid 1: SQL Injection in login API
@app.route("/api/login", methods=["POST"])
def api_login():
    """
    SQL Injection vulnerability for DAST testing
    """
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # Kwetsbare SQL-query zonder parameters - SQL INJECTION
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        result = c.execute(query).fetchone()
        conn.close()

        if result:
            return jsonify(
                {
                    "status": "success",
                    "user_id": result[0],
                    "username": result[1],
                    "role": result[2],
                }
            )
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500


# Kwetsbaarheid 2: Insecure Direct Object Reference (IDOR)
@app.route("/api/users")
def api_users():
    """
    IDOR vulnerability - no access control
    """
    user_id = request.args.get("id", "1")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # IDOR vulnerability - geen SQL injection hier, maar wel IDOR
    c.execute(f"SELECT id, username, email, role FROM users WHERE id = {user_id}")
    row = c.fetchone()
    conn.close()

    if row:
        return jsonify(dict(row))
    else:
        return jsonify({"error": "User not found"}), 404


# API endpoint voor alle users (voor demonstratie)
@app.route("/api/users/all")
def api_all_users():
    """
    Returns all users - no authentication required
    """
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM users")
    rows = c.fetchall()
    conn.close()

    users = [dict(row) for row in rows]
    return jsonify({"users": users})


# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
