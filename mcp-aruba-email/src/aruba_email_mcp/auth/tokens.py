"""Stateless signed tokens (HMAC-SHA256).

A token is `base64url(json_payload).base64url(signature)`. Because it carries and
verifies its own claims, no server-side storage is needed — tokens keep validating
across restarts as long as the signing key is stable. No external dependencies.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time


def _b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64d(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _signature(body: str, key: str) -> str:
    return _b64e(hmac.new(key.encode(), body.encode(), hashlib.sha256).digest())


def sign(payload: dict, key: str) -> str:
    body = _b64e(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    return f"{body}.{_signature(body, key)}"


def verify(token: str, key: str) -> dict | None:
    """Return the payload if the signature is valid and unexpired, else None."""
    if not token or "." not in token:
        return None
    body, _, sig = token.partition(".")
    if not hmac.compare_digest(sig, _signature(body, key)):
        return None
    try:
        payload = json.loads(_b64d(body))
    except Exception:
        return None
    exp = payload.get("exp")
    if exp is not None and exp < time.time():
        return None
    return payload
