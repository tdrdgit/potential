"""The password-gated consent screen used during the OAuth authorization step."""

from __future__ import annotations

import html
import secrets

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from ..config import Settings
from .provider import ArubaOAuthProvider


def _page(txn: str, error: str | None = None) -> str:
    safe_txn = html.escape(txn)
    error_html = (
        f'<p class="error">{html.escape(error)}</p>' if error else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Authorize mailbox access</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
           display: flex; min-height: 100vh; margin: 0; align-items: center;
           justify-content: center; background: #0b0c10; color: #e8e8ea; }}
    .card {{ background: #17181f; padding: 2rem; border-radius: 14px; width: 320px;
            box-shadow: 0 10px 40px rgba(0,0,0,.4); }}
    h1 {{ font-size: 1.15rem; margin: 0 0 .25rem; }}
    p.sub {{ margin: 0 0 1.25rem; color: #a0a0aa; font-size: .85rem; }}
    label {{ display: block; font-size: .8rem; margin-bottom: .35rem; color: #c8c8d0; }}
    input[type=password] {{ width: 100%; padding: .6rem .7rem; border-radius: 8px;
           border: 1px solid #33343d; background: #0f1015; color: #fff; box-sizing: border-box; }}
    button {{ margin-top: 1rem; width: 100%; padding: .65rem; border: 0; border-radius: 8px;
             background: #5b6cff; color: #fff; font-weight: 600; cursor: pointer; }}
    button:hover {{ background: #4a5bef; }}
    .error {{ color: #ff6b6b; font-size: .8rem; margin: .5rem 0 0; }}
  </style>
</head>
<body>
  <form class="card" method="post" action="/login">
    <h1>Authorize mailbox access</h1>
    <p class="sub">Enter the connector password to let Claude access this mailbox.</p>
    <input type="hidden" name="txn" value="{safe_txn}" />
    <label for="password">Connector password</label>
    <input id="password" name="password" type="password" autofocus autocomplete="current-password" />
    {error_html}
    <button type="submit">Authorize</button>
  </form>
</body>
</html>"""


def make_login_routes(provider: ArubaOAuthProvider, settings: Settings):
    async def login_get(request: Request) -> Response:
        txn = request.query_params.get("txn", "")
        if not txn or provider.load_transaction(txn) is None:
            return HTMLResponse(
                _page("", error="This authorization link is invalid or has expired. Start again from Claude."),
                status_code=400,
            )
        return HTMLResponse(_page(txn))

    async def login_post(request: Request) -> Response:
        form = await request.form()
        txn = str(form.get("txn", ""))
        password = str(form.get("password", ""))

        if not txn or provider.load_transaction(txn) is None:
            return HTMLResponse(
                _page("", error="This authorization request expired. Start again from Claude."),
                status_code=400,
            )

        if not secrets.compare_digest(password, settings.admin_login_password):
            return HTMLResponse(_page(txn, error="Incorrect password."), status_code=401)

        redirect_url = await provider.complete_authorization(txn)
        return RedirectResponse(url=redirect_url, status_code=302)

    return login_get, login_post
