
from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)


@app.before_request
def before_request():
    if request.path != "/metrics":
        request.start_time = time.time()


@app.after_request
def after_request(response):
    if request.path != "/metrics":
        duration = time.time() - request.start_time

        REQUEST_COUNT.labels(
            request.method,
            request.endpoint or "unknown",
            response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            request.method,
            request.endpoint or "unknown"
        ).observe(duration)

    return response


@app.route("/")
def home():
    return jsonify({
        "application": "DevOps Status API",
        "message": "Application is running",
        "version": "1.0.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
