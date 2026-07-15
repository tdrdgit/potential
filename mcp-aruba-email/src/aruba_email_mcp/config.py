"""Runtime configuration, loaded from environment variables (or a local .env).

All secrets (Aruba password, admin password) come from the environment — nothing
sensitive is hard-coded or committed. See `.env.example` for the full list.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Public HTTPS base URL (OAuth issuer / where Claude reaches this server).
    # Optional: on Render this is auto-derived from RENDER_EXTERNAL_URL.
    public_base_url: AnyHttpUrl | None = None
    # Automatically injected by Render (https://<service>.onrender.com).
    render_external_url: str | None = None

    # Aruba mailbox credentials (server-side only).
    aruba_email: str
    aruba_password: str
    aruba_imap_host: str = "imaps.aruba.it"
    aruba_imap_port: int = 993
    aruba_smtp_host: str = "smtps.aruba.it"
    aruba_smtp_port: int = 465
    aruba_drafts_folder: str = "Drafts"
    aruba_sent_folder: str = "Sent"

    # Consent-screen gate for the OAuth flow.
    admin_login_password: str

    # Runtime.
    data_dir: str = "./data"
    host: str = "0.0.0.0"
    port: int = 8000

    # OAuth lifetimes (seconds).
    txn_ttl: int = 600
    auth_code_ttl: int = 300
    access_token_ttl: int = 3600
    refresh_token_ttl: int = 60 * 60 * 24 * 30

    # Single logical scope for this personal connector.
    mailbox_scope: str = "mailbox"

    @property
    def base_url(self) -> str:
        """Issuer/base URL as a string, without a trailing slash.

        Prefers PUBLIC_BASE_URL; falls back to Render's RENDER_EXTERNAL_URL so
        the server "just works" on Render with no manual URL configuration.
        """
        raw = str(self.public_base_url) if self.public_base_url else self.render_external_url
        if not raw:
            raise RuntimeError(
                "Set PUBLIC_BASE_URL to the server's public https URL "
                "(on Render this is provided automatically)."
            )
        return raw.rstrip("/")

    @property
    def issuer_url(self) -> AnyHttpUrl:
        return AnyHttpUrl(self.base_url)

    @property
    def resource_url(self) -> AnyHttpUrl:
        return AnyHttpUrl(f"{self.base_url}/mcp")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
