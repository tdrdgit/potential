"""SMTP send access to the Aruba mailbox (blocking; call from a worker thread)."""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .config import Settings
from .imap_client import ImapClient
from .mailbuild import build_message, build_reply


def _sender_domain(email_addr: str) -> str | None:
    return email_addr.split("@", 1)[1] if "@" in email_addr else None


class SmtpClient:
    """Sends mail through Aruba's SMTP over implicit TLS (port 465)."""

    def __init__(self, settings: Settings):
        self._s = settings

    def _deliver(self, msg: EmailMessage) -> str:
        with smtplib.SMTP_SSL(self._s.aruba_smtp_host, self._s.aruba_smtp_port) as smtp:
            smtp.login(self._s.aruba_email, self._s.aruba_password)
            smtp.send_message(msg)
        return msg["Message-ID"] or ""

    def _save_sent_copy(self, msg: EmailMessage) -> None:
        """Best-effort: keep a copy in the Sent folder (never fatal)."""
        try:
            with ImapClient(self._s) as imap:
                folder = imap.resolve_special_folder("\\Sent", self._s.aruba_sent_folder)
                imap.append_message(msg.as_bytes(), folder, flags=r"(\Seen)")
        except Exception:
            pass

    def send(
        self,
        to: list[str],
        subject: str,
        body_text: str,
        body_html: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ) -> dict:
        msg = build_message(
            sender=self._s.aruba_email,
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            cc=cc,
            bcc=bcc,
            domain=_sender_domain(self._s.aruba_email),
        )
        message_id = self._deliver(msg)
        self._save_sent_copy(msg)
        return {"status": "sent", "message_id": message_id, "to": to, "subject": subject}

    def reply(
        self,
        uid: str,
        body_text: str,
        folder: str = "INBOX",
        reply_all: bool = False,
        body_html: str | None = None,
    ) -> dict:
        with ImapClient(self._s) as imap:
            original = imap.get_message_object(uid, folder)
        msg = build_reply(
            original=original,  # type: ignore[arg-type]
            sender=self._s.aruba_email,
            body_text=body_text,
            reply_all=reply_all,
            body_html=body_html,
            domain=_sender_domain(self._s.aruba_email),
        )
        message_id = self._deliver(msg)
        self._save_sent_copy(msg)
        return {
            "status": "sent",
            "message_id": message_id,
            "in_reply_to": msg["In-Reply-To"],
            "to": msg["To"],
            "subject": msg["Subject"],
        }

    def create_draft(
        self,
        to: list[str],
        subject: str,
        body_text: str,
        body_html: str | None = None,
        cc: list[str] | None = None,
    ) -> dict:
        msg = build_message(
            sender=self._s.aruba_email,
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            cc=cc,
            domain=_sender_domain(self._s.aruba_email),
        )
        with ImapClient(self._s) as imap:
            folder = imap.resolve_special_folder("\\Drafts", self._s.aruba_drafts_folder)
            imap.append_message(msg.as_bytes(), folder, flags=r"(\Draft)")
        return {"status": "draft_saved", "folder": folder, "subject": subject}
