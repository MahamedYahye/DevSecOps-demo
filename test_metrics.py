from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
# registreer *alleen* de metrics-exporter vóór routes
PrometheusMetrics(app, path="/metrics")

@app.route("/")
def hello():
    return "ok"

if __name__ == "__main__":
    app.run(port=5005)
