from flask import Flask, request, render_template, redirect, session, jsonify
import sqlite3
import os
import time
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.secret_key = "zeer_zwakke_sleutel"  # Duidelijkere zwakke sleutel

# Verbeterde Prometheus configuratie
metrics = PrometheusMetrics(app, path='/metrics')

# Custom metrics toevoegen
metrics.info('app_info', 'Flask applicatie informatie', version='1.0.0')

# Request duration metric
metrics.histogram(
    'request_duration_seconds', 'Flask HTTP request duration in seconds',
    labels={'endpoint': lambda: request.endpoint, 'method': lambda: request.method}
)

# Request counter per endpoint
endpoints_counter = metrics.counter(
    'requests_by_endpoint', 'Number of requests per endpoint',
    labels={'endpoint': lambda: request.endpoint, 'method': lambda: request.method}
)

# Database operatie timer
database_ops_time = metrics.histogram(
    'database_operation_seconds', 'SQLite database operation time in seconds'
)

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
@endpoints_counter
def home():
    return render_template("home.html")


# Kwetsbaarheid 1: SQL Injectie
@app.route("/login", methods=["GET", "POST"])
@endpoints_counter
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Kwetsbare SQL-query zonder parameters
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        
        # Database operatie timen met Prometheus
        with database_ops_time.time():
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
@endpoints_counter
def search():
    query = request.args.get("q", "")
    return render_template("search.html", query=query)


# Kwetsbaarheid 3: Server-Side Template Injection (SSTI)
@app.route("/profile")
@endpoints_counter
def profile():
    if "logged_in" not in session:
        return redirect("/login")
    return render_template("profile.html", time=time.ctime())


# Kwetsbaarheid 4: Insecure Direct Object Reference (IDOR)
@app.route("/api/users")
@endpoints_counter
def api_users():
    user_id = request.args.get("id", "1")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    with database_ops_time.time():
        c.execute(f"SELECT id, username FROM users WHERE id = {user_id}")
        user = dict(c.fetchone())
    
    conn.close()

    return jsonify(user)


# Kwetsbaarheid 5: Security Misconfiguration (geen rate limiting)
@app.route("/api/login", methods=["POST"])
@endpoints_counter
def api_login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    with database_ops_time.time():
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
@endpoints_counter
def test_route():
    return render_template("Test.html")  # Let op: hoofdletter T in Test.html


# Gezondheidscheck endpoint toevoegen voor Kubernetes liveness probe
@app.route("/health")
@metrics.do_not_track()  # Niet meetellen in metrics
def health_check():
    return jsonify({"status": "healthy"}), 200


# Extra metric endpoints voor specifieke monitoring
@app.route("/metrics/database")
@metrics.do_not_track()
def database_metrics():
    # Een extra endpoint dat specifieke database stats kan teruggeven
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    with database_ops_time.time():
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "user_count": user_count,
        "database_name": "database.db",
        "status": "online"
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# AWS key verwijderen uit code (dit zou in een veilige omgevingsvariabele moeten)
# AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"