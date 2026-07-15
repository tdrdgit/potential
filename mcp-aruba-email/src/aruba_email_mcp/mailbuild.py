"""Pure MIME-building helpers (no network), unit-testable in isolation."""

from __future__ import annotations

from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from .mailparse import best_effort_text, decode_mime_header


def build_message(
    *,
    sender: str,
    to: list[str],
    subject: str,
    body_text: str,
    body_html: str | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    in_reply_to: str | None = None,
    references: str | None = None,
    domain: str | None = None,
) -> EmailMessage:
    """Construct an EmailMessage with a text (and optional HTML) body."""
    msg = EmailMessage()
    msg["From"] = sender
    if to:
        msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=domain)
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references

    msg.set_content(body_text or "")
    if body_html:
        msg.add_alternative(body_html, subtype="html")
    return msg


def _reply_subject(original_subject: str) -> str:
    subj = (original_subject or "").strip()
    if subj.lower().startswith("re:"):
        return subj
    return f"Re: {subj}" if subj else "Re:"


def _quote_body(original_text: str, original_from: str) -> str:
    quoted = "\n".join("> " + line for line in original_text.splitlines())
    attribution = f"On previous message, {original_from} wrote:" if original_from else "Previously wrote:"
    return f"{attribution}\n{quoted}"


def build_reply(
    *,
    original: EmailMessage,
    sender: str,
    body_text: str,
    reply_all: bool = False,
    body_html: str | None = None,
    domain: str | None = None,
) -> EmailMessage:
    """Build a reply to `original`, threading headers set correctly."""
    original_from_hdr = original["From"] or ""
    reply_to_hdr = original["Reply-To"] or original_from_hdr
    to = [reply_to_hdr] if reply_to_hdr else []

    cc: list[str] = []
    if reply_all:
        extra = []
        if original["To"]:
            extra.append(str(original["To"]))
        if original["Cc"]:
            extra.append(str(original["Cc"]))
        cc = [e for e in extra if e]

    orig_msg_id = original["Message-ID"]
    orig_refs = original["References"]
    references = " ".join(x for x in [str(orig_refs) if orig_refs else "", str(orig_msg_id) if orig_msg_id else ""] if x).strip()

    quoted = _quote_body(best_effort_text(original), decode_mime_header(original_from_hdr))
    full_text = f"{body_text}\n\n{quoted}" if body_text else quoted

    return build_message(
        sender=sender,
        to=to,
        subject=_reply_subject(decode_mime_header(original["Subject"] or "")),
        body_text=full_text,
        body_html=body_html,
        cc=cc or None,
        in_reply_to=str(orig_msg_id) if orig_msg_id else None,
        references=references or None,
        domain=domain,
    )
