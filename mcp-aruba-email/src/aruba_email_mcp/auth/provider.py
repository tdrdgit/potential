"""OAuth 2.1 Authorization Server provider backed by :class:`KVStore`.

The MCP SDK's built-in `/authorize`, `/token`, `/register` and metadata routes
call into this provider. The SDK verifies PKCE, redirect_uri consistency and
client authentication itself (see mcp.server.auth.handlers); this class only
issues/stores/loads clients, codes and tokens.

Access is gated by an admin password: `authorize()` parks the request and
redirects the browser to `/login`, and only `complete_authorization()` — called
after a correct password — mints an authorization code.
"""

from __future__ import annotations

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

from ..config import Settings
from .store import KVStore

NS_CLIENT = "client"
NS_TXN = "txn"
NS_CODE = "code"
NS_ACCESS = "access"
NS_REFRESH = "refresh"

SUBJECT = "mailbox-owner"


class ArubaOAuthProvider(
    OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]
):
    def __init__(self, settings: Settings, store: KVStore):
        self._s = settings
        self._store = store

    # -- clients ------------------------------------------------------------
    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        raw = self._store.get(NS_CLIENT, client_id)
        if raw is None:
            return None
        return OAuthClientInformationFull.model_validate_json(raw)

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

        access_str = secrets.token_urlsafe(32)
        refresh_str = secrets.token_urlsafe(32)
        access_exp = int(time.time()) + self._s.access_token_ttl
        refresh_exp = int(time.time()) + self._s.refresh_token_ttl
        scopes = authorization_code.scopes

        access = AccessToken(
            token=access_str,
            client_id=client.client_id,
            scopes=scopes,
            expires_at=access_exp,
            resource=authorization_code.resource,
            subject=authorization_code.subject,
        )
        refresh = RefreshToken(
            token=refresh_str,
            client_id=client.client_id,
            scopes=scopes,
            expires_at=refresh_exp,
            subject=authorization_code.subject,
        )
        self._store.put(NS_ACCESS, access_str, access.model_dump_json(), expires_at=access_exp)
        self._store.put(NS_REFRESH, refresh_str, refresh.model_dump_json(), expires_at=refresh_exp)

        return OAuthToken(
            access_token=access_str,
            token_type="Bearer",
            expires_in=self._s.access_token_ttl,
            refresh_token=refresh_str,
            scope=" ".join(scopes),
        )

    # -- tokens -------------------------------------------------------------
    async def load_access_token(self, token: str) -> AccessToken | None:
        raw = self._store.get(NS_ACCESS, token)
        if raw is None:
            return None
        access = AccessToken.model_validate_json(raw)
        if access.expires_at and access.expires_at < time.time():
            self._store.delete(NS_ACCESS, token)
            return None
        return access

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        raw = self._store.get(NS_REFRESH, refresh_token)
        if raw is None:
            return None
        return RefreshToken.model_validate_json(raw)

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        # Rotate: invalidate the old refresh token, issue a fresh pair.
        self._store.delete(NS_REFRESH, refresh_token.token)
        issued_scopes = scopes or refresh_token.scopes

        access_str = secrets.token_urlsafe(32)
        new_refresh_str = secrets.token_urlsafe(32)
        access_exp = int(time.time()) + self._s.access_token_ttl
        refresh_exp = int(time.time()) + self._s.refresh_token_ttl

        access = AccessToken(
            token=access_str,
            client_id=client.client_id,
            scopes=issued_scopes,
            expires_at=access_exp,
            subject=refresh_token.subject,
        )
        new_refresh = RefreshToken(
            token=new_refresh_str,
            client_id=client.client_id,
            scopes=issued_scopes,
            expires_at=refresh_exp,
            subject=refresh_token.subject,
        )
        self._store.put(NS_ACCESS, access_str, access.model_dump_json(), expires_at=access_exp)
        self._store.put(NS_REFRESH, new_refresh_str, new_refresh.model_dump_json(), expires_at=refresh_exp)

        return OAuthToken(
            access_token=access_str,
            token_type="Bearer",
            expires_in=self._s.access_token_ttl,
            refresh_token=new_refresh_str,
            scope=" ".join(issued_scopes),
        )

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        # We don't know which bucket it came from; try both.
        self._store.delete(NS_ACCESS, token.token)
        self._store.delete(NS_REFRESH, token.token)
