from flask import Flask, request, render_template, redirect, session, jsonify
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = "zeer_zwakke_sleutel"  # Duidelijkere zwakke sleutel

# Hardcoded API-sleutel
API_KEY = "abcdef1234567890"


# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )"""
    )

    # Sample data met duidelijker hardcoded wachtwoord
    HARDCODED_PASSWORD = "wachtwoord123!"
    c.execute(
        f"INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', '{HARDCODED_PASSWORD}')"
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("home.html")


# Kwetsbaarheid 1: SQL Injectie
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Kwetsbare SQL-query zonder parameters
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = c.execute(query).fetchone()
        conn.close()

        if result:
            session["logged_in"] = True
            session["username"] = username
            return redirect("/profile")
        else:
            error = "Ongeldige inloggegevens. Probeer admin/wachtwoord123!"

    return render_template("login.html", error=error)


# Kwetsbaarheid 2: Cross-Site Scripting (XSS)
@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template("search.html", query=query)


# Kwetsbaarheid 3: Server-Side Template Injection (SSTI)
@app.route("/profile")
def profile():
    if "logged_in" not in session:
        return redirect("/login")
    return render_template("profile.html", time=time.ctime())


# Kwetsbaarheid 4: Insecure Direct Object Reference (IDOR)
@app.route("/api/users")
def api_users():
    user_id = request.args.get("id", "1")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f"SELECT id, username FROM users WHERE id = {user_id}")
    user = dict(c.fetchone())
    conn.close()

    return jsonify(user)


# Kwetsbaarheid 5: Security Misconfiguration (geen rate limiting)
@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    )
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "success", "user_id": result[0]})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route("/Test")
def test_route():
    return render_template("Test.html")  # Let op: hoofdletter T in Test.html


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
