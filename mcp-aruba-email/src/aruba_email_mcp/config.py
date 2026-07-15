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
    public_base_url: AnyHttpUrl

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
        """Issuer/base URL as a string, without a trailing slash."""
        return str(self.public_base_url).rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
