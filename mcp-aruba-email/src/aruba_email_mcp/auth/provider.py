"""OAuth 2.1 Authorization Server provider.

The MCP SDK's built-in `/authorize`, `/token`, `/register` and metadata routes
call into this provider. The SDK verifies PKCE, redirect_uri consistency and
client authentication itself (see mcp.server.auth.handlers).

Access/refresh tokens are **stateless**: they are HMAC-signed self-describing
strings (see `tokens.py`) rather than random values stored in a database. That
way they keep validating across restarts/redeploys — essential on hosts without a
persistent disk (e.g. Render free tier) so the connector never needs
re-authorization. Only short-lived, interactive-login state (authorization codes
and transactions) lives in SQLite, which is fine because it is only used while the
server is awake during the login itself.

Access is gated by an admin password: `authorize()` parks the request and
redirects the browser to `/login`, and only `complete_authorization()` — called
after a correct password — mints an authorization code.
"""

from __future__ import annotations

import logging
import secrets
import time

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    OAuthAuthorizationServerProvider,
    RefreshToken,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from pydantic import AnyUrl

from ..config import Settings
from .store import KVStore
from .tokens import sign, verify

logger = logging.getLogger(__name__)

NS_CLIENT = "client"
NS_TXN = "txn"
NS_CODE = "code"

SUBJECT = "mailbox-owner"

# Placeholder redirect for clients reconstructed after a restart. It is never a
# usable target: a fresh /authorize validates the request redirect_uri against
# this list (and would fail), so a reconstructed client can only serve the
# refresh-token grant — which does not use redirect_uri.
_UNUSED_REDIRECT = "http://localhost/oauth-unused"

# Process-lifetime fallback signing key (used only if OAUTH_SIGNING_KEY is unset).
_EPHEMERAL_KEY: str | None = None


def _signing_key(settings: Settings) -> str:
    global _EPHEMERAL_KEY
    if settings.oauth_signing_key:
        return settings.oauth_signing_key
    if _EPHEMERAL_KEY is None:
        _EPHEMERAL_KEY = secrets.token_urlsafe(32)
        logger.warning(
            "OAUTH_SIGNING_KEY is not set — using an ephemeral key. Tokens will "
            "NOT survive a restart; set OAUTH_SIGNING_KEY for persistence."
        )
    return _EPHEMERAL_KEY


class ArubaOAuthProvider(
    OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]
):
    def __init__(self, settings: Settings, store: KVStore):
        self._s = settings
        self._store = store

    # -- clients ------------------------------------------------------------
    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        raw = self._store.get(NS_CLIENT, client_id)
        if raw is not None:
            return OAuthClientInformationFull.model_validate_json(raw)
        # Not in storage (e.g. lost on a free-tier restart). Reconstruct a minimal
        # PUBLIC client so the refresh-token grant keeps working. It has no usable
        # redirect and no secret, so it cannot start a new authorization — only the
        # holder of a validly-signed refresh token benefits.
        return OAuthClientInformationFull(
            client_id=client_id,
            client_secret=None,
            redirect_uris=[AnyUrl(_UNUSED_REDIRECT)],
            token_endpoint_auth_method="none",
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope=self._s.mailbox_scope,
        )

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        self._store.put(NS_CLIENT, client_info.client_id, client_info.model_dump_json())

    # -- authorization ------------------------------------------------------
    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        """Park the request and send the browser to the password gate."""
        txn_id = secrets.token_urlsafe(24)
        payload = {
            "client_id": client.client_id,
            "params": params.model_dump(mode="json"),
        }
        import json

        self._store.put(
            NS_TXN,
            txn_id,
            json.dumps(payload),
            expires_at=time.time() + self._s.txn_ttl,
        )
        return f"{self._s.base_url}/login?txn={txn_id}"

    def load_transaction(self, txn_id: str) -> dict | None:
        import json

        raw = self._store.get(NS_TXN, txn_id)
        return json.loads(raw) if raw else None

    async def complete_authorization(self, txn_id: str) -> str:
        """Called after a correct admin password: mint a code, return redirect."""
        payload = self.load_transaction(txn_id)
        if payload is None:
            raise ValueError("Authorization request expired or unknown. Please retry from Claude.")
        params = AuthorizationParams.model_validate(payload["params"])
        client_id = payload["client_id"]

        code = secrets.token_urlsafe(32)
        scopes = params.scopes or [self._s.mailbox_scope]
        auth_code = AuthorizationCode(
            code=code,
            scopes=scopes,
            expires_at=time.time() + self._s.auth_code_ttl,
            client_id=client_id,
            code_challenge=params.code_challenge,
            redirect_uri=params.redirect_uri,
            redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
            resource=params.resource,
            subject=SUBJECT,
        )
        self._store.put(
            NS_CODE, code, auth_code.model_dump_json(), expires_at=auth_code.expires_at
        )
        self._store.delete(NS_TXN, txn_id)

        return construct_redirect_uri(
            str(params.redirect_uri), code=code, state=params.state
        )

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        raw = self._store.get(NS_CODE, authorization_code)
        if raw is None:
            return None
        return AuthorizationCode.model_validate_json(raw)

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        self._store.delete(NS_CODE, authorization_code.code)
        return self._issue_tokens(
            client_id=client.client_id,
            scopes=authorization_code.scopes,
            subject=authorization_code.subject or SUBJECT,
            resource=authorization_code.resource,
        )

    # -- tokens (stateless, signed) ----------------------------------------
    def _issue_tokens(
        self, *, client_id: str, scopes: list[str], subject: str, resource: str | None
    ) -> OAuthToken:
        key = _signing_key(self._s)
        now = int(time.time())
        access = sign(
            {
                "t": "access",
                "cid": client_id,
                "scopes": scopes,
                "sub": subject,
                "res": resource,
                "exp": now + self._s.access_token_ttl,
            },
            key,
        )
        refresh = sign(
            {
                "t": "refresh",
                "cid": client_id,
                "scopes": scopes,
                "sub": subject,
                "exp": now + self._s.refresh_token_ttl,
            },
            key,
        )
        return OAuthToken(
            access_token=access,
            token_type="Bearer",
            expires_in=self._s.access_token_ttl,
            refresh_token=refresh,
            scope=" ".join(scopes),
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        payload = verify(token, _signing_key(self._s))
        if payload is None or payload.get("t") != "access":
            return None
        return AccessToken(
            token=token,
            client_id=payload["cid"],
            scopes=payload.get("scopes", []),
            expires_at=payload.get("exp"),
            resource=payload.get("res"),
            subject=payload.get("sub"),
        )

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        payload = verify(refresh_token, _signing_key(self._s))
        if payload is None or payload.get("t") != "refresh":
            return None
        return RefreshToken(
            token=refresh_token,
            client_id=payload["cid"],
            scopes=payload.get("scopes", []),
            expires_at=payload.get("exp"),
            subject=payload.get("sub"),
        )

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        return self._issue_tokens(
            client_id=client.client_id,
            scopes=scopes or refresh_token.scopes,
            subject=refresh_token.subject or SUBJECT,
            resource=None,
        )

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        # Tokens are stateless (not stored), so there's nothing to delete here.
        # To revoke everything, rotate OAUTH_SIGNING_KEY (invalidates all tokens).
        return None
