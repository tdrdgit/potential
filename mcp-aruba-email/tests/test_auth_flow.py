"""End-to-end OAuth flow test using an in-process Starlette TestClient.

Exercises DCR -> authorize -> password login -> token, plus that /mcp is
protected (401 without a token) and that all mailbox tools are registered.
No Aruba connection is made.
"""

import base64
import hashlib
import os
from urllib.parse import parse_qs, urlparse

import pytest
from starlette.testclient import TestClient

ADMIN_PASSWORD = "test-admin-password"
REDIRECT_URI = "http://localhost:9999/callback"


@pytest.fixture(scope="module")
def app_and_mcp(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data")
    os.environ.update(
        {
            "PUBLIC_BASE_URL": "https://mail-mcp.test.example",
            "ARUBA_EMAIL": "carlo@potential.contractors",
            "ARUBA_PASSWORD": "unused-in-this-test",
            "ADMIN_LOGIN_PASSWORD": ADMIN_PASSWORD,
            "OAUTH_SIGNING_KEY": "stable-test-signing-key",
            "DATA_DIR": str(data_dir),
        }
    )
    from aruba_email_mcp.config import get_settings

    get_settings.cache_clear()
    from aruba_email_mcp.server import build_mcp

    mcp = build_mcp()
    return mcp.streamable_http_app(), mcp


@pytest.fixture(scope="module")
def client(app_and_mcp):
    app, _ = app_and_mcp
    # Enter the context manager so the Streamable HTTP session manager
    # (and its task group) is started via the app lifespan.
    with TestClient(app, follow_redirects=False) as c:
        yield c


def _pkce():
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return verifier, challenge


def test_metadata_endpoints(client):
    r = client.get("/.well-known/oauth-authorization-server")
    assert r.status_code == 200
    meta = r.json()
    assert meta["authorization_endpoint"].endswith("/authorize")
    assert meta["token_endpoint"].endswith("/token")
    assert meta["registration_endpoint"].endswith("/register")

    r2 = client.get("/.well-known/oauth-protected-resource/mcp")
    assert r2.status_code == 200
    assert "authorization_servers" in r2.json()


def test_mcp_requires_auth(client):
    r = client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        headers={"Accept": "application/json, text/event-stream"},
    )
    assert r.status_code == 401


def test_full_oauth_flow(client):
    # 1. Dynamic Client Registration
    reg = client.post(
        "/register",
        json={
            "redirect_uris": [REDIRECT_URI],
            "token_endpoint_auth_method": "none",
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "client_name": "Test Client",
        },
    )
    assert reg.status_code == 201, reg.text
    client_id = reg.json()["client_id"]

    # 2. Authorize -> should redirect to the /login gate with a txn.
    verifier, challenge = _pkce()
    auth = client.get(
        "/authorize",
        params={
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": "xyz-state",
        },
    )
    assert auth.status_code == 302, auth.text
    login_location = auth.headers["location"]
    txn = parse_qs(urlparse(login_location).query)["txn"][0]

    # 3a. Wrong password is rejected.
    bad = client.post("/login", data={"txn": txn, "password": "nope"})
    assert bad.status_code == 401

    # 3b. Correct password -> redirect back to client with a code.
    good = client.post("/login", data={"txn": txn, "password": ADMIN_PASSWORD})
    assert good.status_code == 302, good.text
    cb = urlparse(good.headers["location"])
    qs = parse_qs(cb.query)
    assert qs["state"][0] == "xyz-state"
    code = qs["code"][0]

    # 4. Exchange the code (with PKCE verifier) for tokens.
    tok = client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "code_verifier": verifier,
        },
    )
    assert tok.status_code == 200, tok.text
    token = tok.json()
    assert token["token_type"] == "Bearer"
    assert token["access_token"]
    assert token["refresh_token"]

    # 5. The access token must be accepted by the protected /mcp endpoint
    #    (i.e. no longer 401). A bare POST may 400 on protocol, but not 401.
    authed = client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}},
        headers={
            "Authorization": f"Bearer {token['access_token']}",
            "Accept": "application/json, text/event-stream",
        },
    )
    assert authed.status_code != 401

    # 6. Wrong PKCE verifier must fail (fresh code).
    verifier2, challenge2 = _pkce()
    auth2 = client.get(
        "/authorize",
        params={
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "code_challenge": challenge2,
            "code_challenge_method": "S256",
            "state": "s2",
        },
    )
    txn2 = parse_qs(urlparse(auth2.headers["location"]).query)["txn"][0]
    good2 = client.post("/login", data={"txn": txn2, "password": ADMIN_PASSWORD})
    code2 = parse_qs(urlparse(good2.headers["location"]).query)["code"][0]
    bad_tok = client.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code2,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "code_verifier": "wrong-verifier",
        },
    )
    assert bad_tok.status_code == 400


@pytest.mark.anyio
async def test_tools_registered(app_and_mcp):
    _, mcp = app_and_mcp
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert {
        "list_recent_emails",
        "list_unread_emails",
        "search_emails",
        "get_email",
        "list_folders",
        "mark_email_read",
        "move_email",
        "create_folder",
        "get_email_rules",
        "send_email",
        "reply_to_email",
        "create_draft",
    } == names


@pytest.fixture
def anyio_backend():
    return "asyncio"
