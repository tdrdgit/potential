"""ASGI application factory for running under uvicorn/gunicorn.

    uvicorn aruba_email_mcp.asgi:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from .server import build_mcp

app = build_mcp().streamable_http_app()
