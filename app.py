# # from flask import Flask, request, render_template, redirect, session, jsonify
# # import sqlite3
# # import os
# # import time
# # from prometheus_flask_exporter import PrometheusMetrics

# # app = Flask(__name__)
# # app.secret_key = "zeer_zwakke_sleutel"  # Duidelijkere zwakke sleutel
# # metrics = PrometheusMetrics(app)

# # # Hardcoded API-sleutel
# # API_KEY = "abcdef1234567890"


# # # Database setup
# # def init_db():
# #     conn = sqlite3.connect("database.db")
# #     c = conn.cursor()
# #     c.execute(
# #         """
# #     CREATE TABLE IF NOT EXISTS users (
# #         id INTEGER PRIMARY KEY,
# #         username TEXT,
# #         password TEXT
# #     )"""
# #     )

# #     # Sample data met duidelijker hardcoded wachtwoord
# #     HARDCODED_PASSWORD = "wachtwoord123!"
# #     c.execute(
# #         f"INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', '{HARDCODED_PASSWORD}')"
# #     )
# #     conn.commit()
# #     conn.close()


# # @app.route("/")
# # def home():
# #     return render_template("home.html")


# # # Kwetsbaarheid 1: SQL Injectie
# # @app.route("/login", methods=["GET", "POST"])
# # def login():
# #     error = None
# #     if request.method == "POST":
# #         username = request.form["username"]
# #         password = request.form["password"]

# #         # Kwetsbare SQL-query zonder parameters
# #         conn = sqlite3.connect("database.db")
# #         c = conn.cursor()
# #         query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
# #         result = c.execute(query).fetchone()
# #         conn.close()

# #         if result:
# #             session["logged_in"] = True
# #             session["username"] = username
# #             return redirect("/profile")
# #         else:
# #             error = "Ongeldige inloggegevens. Probeer admin/wachtwoord123!"

# #     return render_template("login.html", error=error)


# # # Kwetsbaarheid 2: Cross-Site Scripting (XSS)
# # @app.route("/search")
# # def search():
# #     query = request.args.get("q", "")
# #     return render_template("search.html", query=query)


# # # Kwetsbaarheid 3: Server-Side Template Injection (SSTI)
# # @app.route("/profile")
# # def profile():
# #     if "logged_in" not in session:
# #         return redirect("/login")
# #     return render_template("profile.html", time=time.ctime())


# # # Kwetsbaarheid 4: Insecure Direct Object Reference (IDOR)
# # @app.route("/api/users")
# # def api_users():
# #     user_id = request.args.get("id", "1")

# #     conn = sqlite3.connect("database.db")
# #     conn.row_factory = sqlite3.Row
# #     c = conn.cursor()
# #     c.execute(f"SELECT id, username FROM users WHERE id = {user_id}")
# #     user = dict(c.fetchone())
# #     conn.close()

# #     return jsonify(user)


# # # Kwetsbaarheid 5: Security Misconfiguration (geen rate limiting)
# # @app.route("/api/login", methods=["POST"])
# # def api_login():
# #     username = request.json.get("username", "")
# #     password = request.json.get("password", "")

# #     conn = sqlite3.connect("database.db")
# #     c = conn.cursor()
# #     c.execute(
# #         "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
# #     )
# #     result = c.fetchone()
# #     conn.close()

# #     if result:
# #         return jsonify({"status": "success", "user_id": result[0]})
# #     else:
# #         return jsonify({"status": "error", "message": "Invalid credentials"}), 401


# # @app.route("/Test")
# # def test_route():
# #     return render_template("Test.html")  # Let op: hoofdletter T in Test.html


# # if __name__ == "__main__":
# #     init_db()
# #     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
# # AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
# import logging
# from flask import Flask, request, render_template, redirect, session, jsonify
# import sqlite3
# import os
# import time
# from prometheus_flask_exporter import PrometheusMetrics

# app = Flask(__name__)
# app.secret_key = "zeer_zwakke_sleutel"

# # Zet debug-logging aan voor inzicht in registratie en fouten
# app.logger.setLevel(logging.DEBUG)

# # Registreer de Prometheus-exporter vóór al je routes
# metrics = PrometheusMetrics(app, path="/metrics")
# # Optioneel: basis‐info metric
# metrics.info("app_info", "Applicatie metadata", version="1.0.0")

# # Database setup
# def init_db():
#     conn = sqlite3.connect("database.db")
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             username TEXT,
#             password TEXT
#         )
#     """)
#     HARDCODED_PASSWORD = "wachtwoord123!"
#     c.execute(
#         "INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)",
#         (1, "admin", HARDCODED_PASSWORD)
#     )
#     conn.commit()
#     conn.close()

# # Routes
# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     error = None
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database.db")
#         c = conn.cursor()
#         query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
#         result = c.execute(query).fetchone()
#         conn.close()
#         if result:
#             session["logged_in"] = True
#             session["username"] = username
#             return redirect("/profile")
#         else:
#             error = "Ongeldige inloggegevens. Probeer admin/wachtwoord123!"
#     return render_template("login.html", error=error)

# @app.route("/search")
# def search():
#     query = request.args.get("q", "")
#     return render_template("search.html", query=query)

# @app.route("/profile")
# def profile():
#     if not session.get("logged_in"):
#         return redirect("/login")
#     return render_template("profile.html", time=time.ctime())

# @app.route("/api/users")
# def api_users():
#     user_id = request.args.get("id", "1")
#     conn = sqlite3.connect("database.db")
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#     c.execute(f"SELECT id, username FROM users WHERE id = {user_id}")
#     row = c.fetchone()
#     conn.close()
#     return jsonify(dict(row)) if row else (jsonify({}), 200)

# @app.route("/api/login", methods=["POST"])
# def api_login():
#     data = request.get_json() or {}
#     username = data.get("username", "")
#     password = data.get("password", "")
#     conn = sqlite3.connect("database.db")
#     c = conn.cursor()
#     c.execute(
#         "SELECT id FROM users WHERE username = ? AND password = ?",
#         (username, password)
#     )
#     result = c.fetchone()
#     conn.close()
#     if result:
#         return jsonify({"status": "success", "user_id": result[0]})
#     return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# @app.route("/Test")
# def test_route():
#     return render_template("Test.html")

# if __name__ == "__main__":
#     init_db()
#     # Print ingeladen routes voor debugging
#     print(app.url_map)
#     # Start op poort 5001 (pas aan met PORT env var indien gewenst)
#     port = int(os.environ.get("PORT", 5000))
#     # Zet use_reloader=False om metrics actief te houden in debug mode
#     app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
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
API_KEY = "abcdef1234567890"
HARDCODED_PASSWORD = "wachtwoord123!"


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
