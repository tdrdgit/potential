"""IMAP read access to the Aruba mailbox (blocking; call from a worker thread)."""

from __future__ import annotations

import imaplib
import re
from datetime import date, datetime
from email.message import Message
from email.parser import BytesParser
from email.policy import default as default_policy

from .config import Settings
from .mailparse import (
    decode_mime_header,
    format_addresses,
    list_attachments,
    make_snippet,
    parse_date,
)

_LIST_RE = re.compile(r'\((?P<flags>[^)]*)\)\s+(?P<delim>"[^"]*"|NIL)\s+(?P<name>.*)')
_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _to_imap_date(value: str) -> str:
    """Convert an ISO date (YYYY-MM-DD) to IMAP SINCE format (DD-Mon-YYYY)."""
    d = date.fromisoformat(value[:10])
    return f"{d.day:02d}-{_MONTHS[d.month - 1]}-{d.year}"


def _quote_folder(name: str) -> str:
    return '"' + name.replace('"', '\\"') + '"'


class ImapClient:
    """Context-managed IMAP4_SSL connection. Blocking — run in a thread."""

    def __init__(self, settings: Settings):
        self._s = settings
        self.conn: imaplib.IMAP4_SSL | None = None

    def __enter__(self) -> "ImapClient":
        self.conn = imaplib.IMAP4_SSL(self._s.aruba_imap_host, self._s.aruba_imap_port)
        self.conn.login(self._s.aruba_email, self._s.aruba_password)
        return self

    def __exit__(self, *exc) -> None:
        if self.conn is not None:
            try:
                self.conn.logout()
            except Exception:
                pass
            self.conn = None

    # -- folders ------------------------------------------------------------
    def list_folders(self) -> list[str]:
        assert self.conn is not None
        typ, data = self.conn.list()
        if typ != "OK":
            raise RuntimeError("Could not list IMAP folders")
        names: list[str] = []
        for line in data or []:
            if not line:
                continue
            decoded = line.decode() if isinstance(line, bytes) else line
            m = _LIST_RE.match(decoded)
            if not m:
                continue
            name = m.group("name").strip()
            if name.startswith('"') and name.endswith('"'):
                name = name[1:-1]
            names.append(name.replace('\\"', '"'))
        return names

    # -- listing ------------------------------------------------------------
    def list_messages(
        self,
        folder: str = "INBOX",
        unseen_only: bool = False,
        limit: int = 20,
        since: str | None = None,
        include_snippet: bool = True,
    ) -> list[dict]:
        assert self.conn is not None
        typ, _ = self.conn.select(_quote_folder(folder), readonly=True)
        if typ != "OK":
            raise RuntimeError(f"Could not open folder '{folder}'")

        criteria: list[str] = []
        if unseen_only:
            criteria.append("UNSEEN")
        if since:
            criteria += ["SINCE", _to_imap_date(since)]
        if not criteria:
            criteria = ["ALL"]

        typ, data = self.conn.uid("SEARCH", None, *criteria)
        if typ != "OK":
            raise RuntimeError("IMAP search failed")
        uids = data[0].split() if data and data[0] else []
        uids = uids[-limit:][::-1]  # newest first

        return [self._summary(uid, folder, include_snippet) for uid in uids]

    def search(
        self,
        folder: str = "INBOX",
        from_addr: str | None = None,
        subject: str | None = None,
        text: str | None = None,
        since: str | None = None,
        unseen_only: bool = False,
        limit: int = 20,
        include_snippet: bool = True,
    ) -> list[dict]:
        assert self.conn is not None
        typ, _ = self.conn.select(_quote_folder(folder), readonly=True)
        if typ != "OK":
            raise RuntimeError(f"Could not open folder '{folder}'")

        criteria: list = []
        if unseen_only:
            criteria.append("UNSEEN")
        if since:
            criteria += ["SINCE", _to_imap_date(since)]
        if from_addr:
            criteria += ["FROM", from_addr]
        if subject:
            criteria += ["SUBJECT", subject]
        if text:
            criteria += ["TEXT", text]
        if not criteria:
            criteria = ["ALL"]

        # Non-ASCII search terms require a charset; use UTF-8 when present.
        needs_charset = any(
            isinstance(c, str) and any(ord(ch) > 127 for ch in c) for c in criteria
        )
        if needs_charset:
            enc = [c.encode("utf-8") if isinstance(c, str) else c for c in criteria]
            typ, data = self.conn.uid("SEARCH", "CHARSET", "UTF-8", *enc)
        else:
            typ, data = self.conn.uid("SEARCH", None, *criteria)
        if typ != "OK":
            raise RuntimeError("IMAP search failed")
        uids = data[0].split() if data and data[0] else []
        uids = uids[-limit:][::-1]
        return [self._summary(uid, folder, include_snippet) for uid in uids]

    # -- single message -----------------------------------------------------
    def get_message(self, uid: str, folder: str = "INBOX") -> dict:
        assert self.conn is not None
        typ, _ = self.conn.select(_quote_folder(folder), readonly=True)
        if typ != "OK":
            raise RuntimeError(f"Could not open folder '{folder}'")

        typ, data = self.conn.uid("FETCH", str(uid), "(FLAGS RFC822)")
        if typ != "OK" or not data or data[0] is None:
            raise RuntimeError(f"Message uid {uid} not found in '{folder}'")

        raw_bytes = b""
        flags: tuple = ()
        for item in data:
            if isinstance(item, tuple):
                raw_bytes = item[1]
                flags = imaplib.ParseFlags(item[0])
        msg = BytesParser(policy=default_policy).parsebytes(raw_bytes)

        from .mailparse import extract_bodies

        text_plain, text_html = extract_bodies(msg)
        return {
            "uid": uid if isinstance(uid, str) else uid.decode(),
            "folder": folder,
            "seen": _has_seen(flags),
            "from": decode_mime_header(msg["From"] or ""),
            "to": format_addresses(msg["To"]),
            "cc": format_addresses(msg["Cc"]),
            "subject": decode_mime_header(msg["Subject"] or ""),
            "date": parse_date(msg["Date"]),
            "message_id": msg["Message-ID"],
            "in_reply_to": msg["In-Reply-To"],
            "body_text": text_plain.strip(),
            "body_html": text_html.strip() if text_html else "",
            "attachments": list_attachments(msg),
        }

    def get_message_object(self, uid: str, folder: str = "INBOX") -> Message:
        """Return the parsed email.message.Message (used to build replies)."""
        assert self.conn is not None
        self.conn.select(_quote_folder(folder), readonly=True)
        typ, data = self.conn.uid("FETCH", str(uid), "(RFC822)")
        if typ != "OK" or not data or data[0] is None:
            raise RuntimeError(f"Message uid {uid} not found in '{folder}'")
        raw_bytes = b""
        for item in data:
            if isinstance(item, tuple):
                raw_bytes = item[1]
        return BytesParser(policy=default_policy).parsebytes(raw_bytes)

    # -- mutations ----------------------------------------------------------
    def mark_seen(self, uid: str, folder: str = "INBOX", seen: bool = True) -> None:
        assert self.conn is not None
        typ, _ = self.conn.select(_quote_folder(folder), readonly=False)
        if typ != "OK":
            raise RuntimeError(f"Could not open folder '{folder}'")
        op = "+FLAGS" if seen else "-FLAGS"
        typ, _ = self.conn.uid("STORE", str(uid), op, r"(\Seen)")
        if typ != "OK":
            raise RuntimeError("Could not update message flags")

    def append_message(self, raw_bytes: bytes, folder: str, flags: str = "") -> None:
        """APPEND a raw message to a folder (e.g. save a draft or sent copy)."""
        assert self.conn is not None
        typ, _ = self.conn.append(_quote_folder(folder), flags, None, raw_bytes)
        if typ != "OK":
            raise RuntimeError(f"Could not append message to '{folder}'")

    # -- internal -----------------------------------------------------------
    def _summary(self, uid: bytes | str, folder: str, include_snippet: bool) -> dict:
        assert self.conn is not None
        uid_s = uid.decode() if isinstance(uid, bytes) else str(uid)
        typ, data = self.conn.uid(
            "FETCH",
            uid_s,
            "(FLAGS BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE MESSAGE-ID)])",
        )
        header_bytes = b""
        flags: tuple = ()
        for item in data or []:
            if isinstance(item, tuple):
                flags = imaplib.ParseFlags(item[0])
                header_bytes = item[1]
        msg = BytesParser(policy=default_policy).parsebytes(header_bytes)

        snippet = ""
        if include_snippet:
            snippet = self._snippet(uid_s)

        return {
            "uid": uid_s,
            "folder": folder,
            "seen": _has_seen(flags),
            "from": decode_mime_header(msg["From"] or ""),
            "to": format_addresses(msg["To"]),
            "subject": decode_mime_header(msg["Subject"] or ""),
            "date": parse_date(msg["Date"]),
            "message_id": msg["Message-ID"],
            "snippet": snippet,
        }

    def _snippet(self, uid_s: str) -> str:
        """Best-effort short preview (approximate; never raises)."""
        assert self.conn is not None
        try:
            typ, data = self.conn.uid("FETCH", uid_s, "(BODY.PEEK[]<0.8192>)")
            raw = b""
            for item in data or []:
                if isinstance(item, tuple):
                    raw = item[1]
            if not raw:
                return ""
            msg = BytesParser(policy=default_policy).parsebytes(raw)
            return make_snippet(msg)
        except Exception:
            return ""


def _has_seen(flags: tuple) -> bool:
    for f in flags:
        name = f.decode() if isinstance(f, bytes) else f
        if name.lower() == r"\seen":
            return True
    return False
