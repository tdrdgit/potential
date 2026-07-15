"""Pure email-parsing helpers (no network).

Kept dependency-free and side-effect-free so they can be unit-tested against
`.eml` fixtures without touching IMAP.
"""

from __future__ import annotations

import re
from email.header import decode_header, make_header
from email.message import Message
from email.utils import getaddresses, parsedate_to_datetime

_WS_RE = re.compile(r"\s+")
_TAG_RE = re.compile(r"<[^>]+>")
_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)


def decode_mime_header(value: str | None) -> str:
    """Decode an RFC 2047 encoded header value to a plain string."""
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def format_addresses(raw: str | None) -> list[str]:
    """Return a list of 'Name <addr>' / 'addr' strings from a header value."""
    if not raw:
        return []
    out: list[str] = []
    for name, addr in getaddresses([raw]):
        name = decode_mime_header(name)
        if name and addr:
            out.append(f"{name} <{addr}>")
        elif addr:
            out.append(addr)
        elif name:
            out.append(name)
    return out


def parse_date(value: str | None) -> str | None:
    """Return an ISO-8601 timestamp for a Date header, or the raw value."""
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        return dt.isoformat() if dt else value
    except Exception:
        return value


def html_to_text(html: str) -> str:
    """Crude HTML -> text: drop scripts/styles/tags, collapse whitespace."""
    if not html:
        return ""
    text = _STYLE_RE.sub(" ", html)
    text = _TAG_RE.sub(" ", text)
    # Common entities.
    for ent, rep in (
        ("&nbsp;", " "),
        ("&amp;", "&"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&quot;", '"'),
        ("&#39;", "'"),
    ):
        text = text.replace(ent, rep)
    return _WS_RE.sub(" ", text).strip()


def _part_text(part: Message) -> str:
    """Best-effort decode of a single (non-multipart) part to text."""
    try:
        payload = part.get_content()
        if isinstance(payload, bytes):
            charset = part.get_content_charset() or "utf-8"
            return payload.decode(charset, "replace")
        return str(payload)
    except Exception:
        raw = part.get_payload(decode=True)
        if raw is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        try:
            return raw.decode(charset, "replace")
        except Exception:
            return raw.decode("utf-8", "replace")


def extract_bodies(msg: Message) -> tuple[str, str]:
    """Return (text_plain, text_html) walking the MIME tree.

    Attachments (parts with a filename / Content-Disposition: attachment) are
    skipped. The first text/plain and first text/html found are returned.
    """
    text_plain = ""
    text_html = ""
    for part in msg.walk():
        if part.is_multipart():
            continue
        content_type = part.get_content_type()
        disposition = (part.get_content_disposition() or "").lower()
        if disposition == "attachment" or part.get_filename():
            continue
        if content_type == "text/plain" and not text_plain:
            text_plain = _part_text(part)
        elif content_type == "text/html" and not text_html:
            text_html = _part_text(part)
    return text_plain, text_html


def best_effort_text(msg: Message) -> str:
    """A readable text body: prefer text/plain, else HTML converted to text."""
    text_plain, text_html = extract_bodies(msg)
    if text_plain.strip():
        return text_plain.strip()
    if text_html.strip():
        return html_to_text(text_html)
    return ""


def make_snippet(msg: Message, limit: int = 200) -> str:
    text = best_effort_text(msg)
    text = _WS_RE.sub(" ", text).strip()
    return text[:limit]


def list_attachments(msg: Message) -> list[dict]:
    """Metadata for attachment parts (filename, content-type, size)."""
    out: list[dict] = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        disposition = (part.get_content_disposition() or "").lower()
        filename = part.get_filename()
        if disposition == "attachment" or filename:
            payload = part.get_payload(decode=True)
            out.append(
                {
                    "filename": decode_mime_header(filename) if filename else None,
                    "content_type": part.get_content_type(),
                    "size": len(payload) if payload else 0,
                }
            )
    return out
