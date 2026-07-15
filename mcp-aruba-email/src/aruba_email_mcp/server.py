"""FastMCP server: registers the mailbox tools and wires up OAuth + HTTP."""

from __future__ import annotations

import os
from pathlib import Path

import anyio
from mcp.server.auth.settings import (
    AuthSettings,
    ClientRegistrationOptions,
    RevocationOptions,
)
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .auth.login import make_login_routes
from .auth.provider import ArubaOAuthProvider
from .auth.store import KVStore
from .config import Settings, get_settings
from .imap_client import ImapClient
from .smtp_client import SmtpClient

_RULES_PATH = Path(__file__).parent / "email_rules.md"


def _load_rules() -> str:
    try:
        return _RULES_PATH.read_text(encoding="utf-8")
    except Exception:
        return ""


EMAIL_RULES = _load_rules()

INSTRUCTIONS = (
    "Tools to read and send email from an Aruba-hosted mailbox over IMAP/SMTP. "
    "Use list_unread_emails / list_recent_emails to check for new mail, get_email "
    "to read a full message by uid, send_email / reply_to_email / create_draft to "
    "write, and mark_email_read / move_email / create_folder to organise. All "
    "actions use the mailbox configured on the server.\n\n"
    "This connector carries the user's project & email rules. When the user asks "
    "for a \"Recap email\" (or to summarise/triage the inbox), FIRST call "
    "get_email_rules and follow the procedure it describes, then wait for "
    "instructions before marking read or moving anything. Active projects: "
    "Mountain Retreat, Blue Lagoon Retreat Improvements, Trenitalia."
)


# --- blocking helpers (offloaded to a worker thread) -----------------------
def _imap_call(settings: Settings, method: str, /, **kwargs):
    with ImapClient(settings) as imap:
        return getattr(imap, method)(**kwargs)


def build_mcp() -> FastMCP:
    settings = get_settings()
    store = KVStore(os.path.join(settings.data_dir, "auth.sqlite"))
    provider = ArubaOAuthProvider(settings, store)

    auth_settings = AuthSettings(
        issuer_url=settings.issuer_url,
        resource_server_url=settings.resource_url,
        client_registration_options=ClientRegistrationOptions(
            enabled=True,
            valid_scopes=[settings.mailbox_scope],
            default_scopes=[settings.mailbox_scope],
        ),
        revocation_options=RevocationOptions(enabled=True),
        required_scopes=None,
    )

    mcp = FastMCP(
        name="Aruba Email",
        instructions=INSTRUCTIONS,
        auth_server_provider=provider,
        auth=auth_settings,
        host=settings.host,
        port=settings.port,
        streamable_http_path="/mcp",
    )

    # -- read tools ---------------------------------------------------------
    @mcp.tool()
    async def list_recent_emails(folder: str = "INBOX", limit: int = 20) -> list[dict]:
        """List the most recent emails in a folder (newest first)."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(settings, "list_messages", folder=folder, limit=limit)
        )

    @mcp.tool()
    async def list_unread_emails(folder: str = "INBOX", limit: int = 20) -> list[dict]:
        """List unread emails in a folder (newest first)."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(
                settings, "list_messages", folder=folder, limit=limit, unseen_only=True
            )
        )

    @mcp.tool()
    async def search_emails(
        from_addr: str | None = None,
        subject: str | None = None,
        text: str | None = None,
        since: str | None = None,
        unseen_only: bool = False,
        folder: str = "INBOX",
        limit: int = 20,
    ) -> list[dict]:
        """Search emails by sender, subject, free text, and/or date (since = YYYY-MM-DD)."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(
                settings,
                "search",
                folder=folder,
                from_addr=from_addr,
                subject=subject,
                text=text,
                since=since,
                unseen_only=unseen_only,
                limit=limit,
            )
        )

    @mcp.tool()
    async def get_email(uid: str, folder: str = "INBOX") -> dict:
        """Fetch the full content of a single email by its uid."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(settings, "get_message", uid=uid, folder=folder)
        )

    @mcp.tool()
    async def list_folders() -> list[str]:
        """List the mailbox's IMAP folders."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(settings, "list_folders")
        )

    @mcp.tool()
    async def mark_email_read(uid: str, folder: str = "INBOX", read: bool = True) -> dict:
        """Mark an email as read (or unread)."""
        await anyio.to_thread.run_sync(
            lambda: _imap_call(settings, "mark_seen", uid=uid, folder=folder, seen=read)
        )
        return {"status": "ok", "uid": uid, "read": read}

    @mcp.tool()
    async def move_email(uid: str, to_folder: str, from_folder: str = "INBOX") -> dict:
        """Move an email to another folder (the folder is created if it doesn't exist)."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(
                settings, "move_message", uid=uid, to_folder=to_folder, from_folder=from_folder
            )
        )

    @mcp.tool()
    async def create_folder(name: str) -> dict:
        """Create a new IMAP folder/mailbox."""
        return await anyio.to_thread.run_sync(
            lambda: _imap_call(settings, "create_folder", name=name)
        )

    @mcp.tool()
    async def get_email_rules() -> str:
        """Return the user's project & email rules (projects, how to attribute mail to
        a project, and the 'Recap email' procedure). Call this before doing a
        'Recap email' or triaging the inbox."""
        return EMAIL_RULES or "No rules file is configured on the server."

    # -- send tools ---------------------------------------------------------
    @mcp.tool()
    async def send_email(
        to: list[str],
        subject: str,
        body_text: str,
        body_html: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ) -> dict:
        """Send a new email from the configured mailbox."""
        smtp = SmtpClient(settings)
        return await anyio.to_thread.run_sync(
            lambda: smtp.send(to, subject, body_text, body_html, cc, bcc)
        )

    @mcp.tool()
    async def reply_to_email(
        uid: str,
        body_text: str,
        folder: str = "INBOX",
        reply_all: bool = False,
        body_html: str | None = None,
    ) -> dict:
        """Reply to an email by uid, with correct threading headers."""
        smtp = SmtpClient(settings)
        return await anyio.to_thread.run_sync(
            lambda: smtp.reply(uid, body_text, folder, reply_all, body_html)
        )

    @mcp.tool()
    async def create_draft(
        to: list[str],
        subject: str,
        body_text: str,
        body_html: str | None = None,
        cc: list[str] | None = None,
    ) -> dict:
        """Create a draft email saved to the mailbox's Drafts folder."""
        smtp = SmtpClient(settings)
        return await anyio.to_thread.run_sync(
            lambda: smtp.create_draft(to, subject, body_text, body_html, cc)
        )

    # -- custom HTTP routes -------------------------------------------------
    login_get, login_post = make_login_routes(provider, settings)
    mcp.custom_route("/login", methods=["GET"])(login_get)
    mcp.custom_route("/login", methods=["POST"])(login_post)

    @mcp.custom_route("/", methods=["GET"])
    async def health(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok", "service": "aruba-email-mcp"})

    return mcp
