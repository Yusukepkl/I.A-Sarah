"""Telemetry integration with Sentry and metrics."""

from __future__ import annotations

import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import sentry_sdk
from prometheus_client import CollectorRegistry, Counter, generate_latest

logger = logging.getLogger(__name__)

REQUESTS_COUNTER = Counter("app_requests_total", "Total HTTP requests")


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: D401
        """Serve metrics."""
        REQUESTS_COUNTER.inc()
        data = generate_latest()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(data)


def init() -> None:
    """Initialize Sentry and start metrics server."""
    dsn = os.getenv("SENTRY_DSN")
    if dsn:
        sentry_sdk.init(dsn=dsn)
        logger.info("Sentry enabled")

    def run_server() -> None:
        httpd = HTTPServer(("0.0.0.0", 8000), MetricsHandler)
        httpd.serve_forever()

    Thread(target=run_server, daemon=True).start()
