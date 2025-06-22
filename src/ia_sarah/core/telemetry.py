"""Telemetry integration with Sentry and metrics."""

from __future__ import annotations

import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from ia_sarah.core.adapters.utils import config_manager as cm

try:
    import sentry_sdk  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    sentry_sdk = None

try:
    from prometheus_client import Counter, generate_latest
except ImportError:  # pragma: no cover - optional dependency
    Counter = None
    generate_latest = None

logger = logging.getLogger(__name__)

if Counter is not None:
    REQUESTS_COUNTER = Counter("app_requests_total", "Total HTTP requests")
else:  # pragma: no cover - optional dependency not installed
    REQUESTS_COUNTER = None


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: D401
        """Serve metrics."""
        if REQUESTS_COUNTER is not None and generate_latest is not None:
            REQUESTS_COUNTER.inc()
            data = generate_latest()
        else:  # pragma: no cover - metrics disabled
            data = b""
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(data)


def init() -> None:
    """Initialize Sentry and start metrics server."""
    config = cm.load_config()
    dsn = os.getenv("SENTRY_DSN") or config.get("sentry_dsn")
    if not os.getenv("PV_KEYWORD_PATH"):
        logger.info("PV_KEYWORD_PATH não definido - modo dummy ativo")
    if dsn and sentry_sdk is not None:
        sentry_sdk.init(dsn=dsn)
        logger.info("Sentry enabled")
    elif dsn:
        logger.warning("SENTRY_DSN set but sentry_sdk not installed")

    if REQUESTS_COUNTER is None:
        logger.warning("prometheus_client não instalado - métricas desativadas")
        return

    def run_server() -> None:
        port_env = os.getenv("METRICS_PORT")
        port = int(port_env or config.get("metrics_port", 8000))
        try:
            httpd = HTTPServer(("0.0.0.0", port), MetricsHandler)
            httpd.serve_forever()
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error("Erro ao iniciar servidor de métricas: %s", exc)

    Thread(target=run_server, daemon=True).start()
