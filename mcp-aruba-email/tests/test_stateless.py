"""Tests that OAuth tokens survive a 'restart' (stateless signing).

Simulates a free-tier restart by throwing away the SQLite store and rebuilding the
provider with a fresh, empty store but the SAME signing key — as happens on Render
when the container recycles but OAUTH_SIGNING_KEY (an env var) stays put.
"""

from aruba_email_mcp.auth.provider import ArubaOAuthProvider
from aruba_email_mcp.auth.store import KVStore
from aruba_email_mcp.auth.tokens import sign, verify
from aruba_email_mcp.config import Settings


def _settings(tmp_path, key="stable-key"):
    return Settings(
        public_base_url="https://mail-mcp.test.example",
        aruba_email="carlo@potential.contractors",
        aruba_password="x",
        admin_login_password="pw",
        oauth_signing_key=key,
        data_dir=str(tmp_path),
    )


def test_sign_verify_roundtrip_and_tamper():
    key = "k1"
    token = sign({"t": "access", "cid": "c", "exp": 9999999999}, key)
    assert verify(token, key)["cid"] == "c"
    # Wrong key rejects.
    assert verify(token, "k2") is None
    # Tampering rejects.
    body, _, sig = token.partition(".")
    assert verify(f"{body}x.{sig}", key) is None


def test_expired_token_rejected():
    assert verify(sign({"t": "access", "exp": 1}, "k"), "k") is None


async def test_access_token_survives_restart(tmp_path):
    settings = _settings(tmp_path)

    store1 = KVStore(str(tmp_path / "a.sqlite"))
    provider1 = ArubaOAuthProvider(settings, store1)
    issued = provider1._issue_tokens(
        client_id="client-1", scopes=["mailbox"], subject="mailbox-owner", resource=None
    )

    # --- simulate restart: brand-new empty store, same signing key ---
    store2 = KVStore(str(tmp_path / "b.sqlite"))
    provider2 = ArubaOAuthProvider(settings, store2)

    access = await provider2.load_access_token(issued.access_token)
    assert access is not None
    assert access.client_id == "client-1"
    assert access.scopes == ["mailbox"]


async def test_refresh_works_after_restart_via_reconstructed_client(tmp_path):
    settings = _settings(tmp_path)
    provider1 = ArubaOAuthProvider(settings, KVStore(str(tmp_path / "a.sqlite")))
    issued = provider1._issue_tokens(
        client_id="client-9", scopes=["mailbox"], subject="mailbox-owner", resource=None
    )

    # Restart: empty store -> the client registration is gone.
    provider2 = ArubaOAuthProvider(settings, KVStore(str(tmp_path / "b.sqlite")))

    # get_client reconstructs a usable public client for the refresh grant.
    client = await provider2.get_client("client-9")
    assert client is not None
    assert client.token_endpoint_auth_method == "none"
    assert client.client_secret is None

    refresh = await provider2.load_refresh_token(client, issued.refresh_token)
    assert refresh is not None and refresh.client_id == "client-9"

    new_tokens = await provider2.exchange_refresh_token(client, refresh, [])
    # The freshly issued access token verifies too.
    access = await provider2.load_access_token(new_tokens.access_token)
    assert access is not None and access.client_id == "client-9"


async def test_token_invalid_under_different_key(tmp_path):
    issued = ArubaOAuthProvider(
        _settings(tmp_path, key="key-A"), KVStore(str(tmp_path / "a.sqlite"))
    )._issue_tokens(client_id="c", scopes=["mailbox"], subject="s", resource=None)

    other = ArubaOAuthProvider(
        _settings(tmp_path, key="key-B"), KVStore(str(tmp_path / "b.sqlite"))
    )
    assert await other.load_access_token(issued.access_token) is None
