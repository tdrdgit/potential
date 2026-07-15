# Aruba Email MCP

A **remote [Model Context Protocol](https://modelcontextprotocol.io) server** that
connects an **Aruba-hosted mailbox** (classic IMAP/SMTP — no native OAuth API) to
Claude as a **custom connector**. Once deployed and added to your Claude account it
works **everywhere**: claude.ai web, the desktop app, the **iPhone/Android apps**,
and Claude Code — in any project, because a remote connector is account-scoped, not
project-scoped.

It exposes **read + send** tools and ships its **own OAuth 2.1 authorization
server**, so no third-party identity provider is required. Access is protected by a
single admin password you choose.

> Your Aruba mailbox password is a **server-side secret**. It is never sent to
> Claude — Claude only ever holds an OAuth token for *this* server.

---

## Tools

**Read (IMAP)**
- `list_recent_emails(folder="INBOX", limit=20)` — newest messages
- `list_unread_emails(folder="INBOX", limit=20)` — unread only
- `search_emails(from_addr, subject, text, since, unseen_only, folder, limit)` — `since` = `YYYY-MM-DD`
- `get_email(uid, folder="INBOX")` — full message (text, HTML, attachments metadata)
- `list_folders()` — IMAP mailboxes
- `mark_email_read(uid, folder="INBOX", read=True)`

**Send (SMTP)**
- `send_email(to, subject, body_text, body_html?, cc?, bcc?)`
- `reply_to_email(uid, body_text, folder="INBOX", reply_all=False, body_html?)` — sets `In-Reply-To`/`References`, quotes original
- `create_draft(to, subject, body_text, body_html?, cc?)` — saved to the Drafts folder

---

## How it works

```
Claude (web / iPhone / desktop / Code)
        │  OAuth 2.1 + PKCE  (token only)
        ▼
  this server  ──IMAP 993 / SMTP 465──▶  Aruba mailbox
   (Streamable HTTP /mcp + built-in OAuth AS)
```

- **Transport:** Streamable HTTP at `POST /mcp`.
- **OAuth endpoints** (auto-mounted by the MCP SDK):
  `/.well-known/oauth-authorization-server`,
  `/.well-known/oauth-protected-resource/mcp`,
  `/authorize`, `/token`, `/register` (Dynamic Client Registration), `/revoke`.
- **Access gate:** `/authorize` parks the request and redirects the browser to
  `/login`, where the **admin password** must be entered before a token is issued.
  Dynamic client registration is open (as the spec expects), but the password means
  a stranger who finds the URL still cannot read your mail.

---

## Configuration

All configuration is via environment variables (see [`.env.example`](.env.example)).
Set secrets through your host's secret manager — **do not commit `.env`**.

| Variable | Required | Default | Notes |
|---|---|---|---|
| `PUBLIC_BASE_URL` | ✅ | — | Public HTTPS base URL (OAuth issuer). No trailing slash. |
| `ARUBA_EMAIL` | ✅ | — | Mailbox address / IMAP+SMTP username. |
| `ARUBA_PASSWORD` | ✅ | — | Mailbox password (server-side secret). |
| `ADMIN_LOGIN_PASSWORD` | ✅ | — | Password typed on the consent screen. |
| `ARUBA_IMAP_HOST` | | `imaps.aruba.it` | |
| `ARUBA_IMAP_PORT` | | `993` | IMAP over SSL. |
| `ARUBA_SMTP_HOST` | | `smtps.aruba.it` | |
| `ARUBA_SMTP_PORT` | | `465` | SMTP over implicit TLS. |
| `ARUBA_DRAFTS_FOLDER` | | `Drafts` | |
| `ARUBA_SENT_FOLDER` | | `Sent` | Sent copies are appended here (best-effort). |
| `DATA_DIR` | | `./data` | Where the OAuth token SQLite DB lives — **mount a volume**. |
| `HOST` / `PORT` | | `0.0.0.0` / `8000` | |

---

## Run locally

```bash
cd mcp-aruba-email
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in real values
python -m aruba_email_mcp   # serves on http://HOST:PORT/mcp
```

Quick checks:

```bash
curl -s localhost:8000/                                         # {"status":"ok",...}
curl -s localhost:8000/.well-known/oauth-authorization-server   # OAuth metadata
```

Run the test suite (offline — no Aruba connection needed):

```bash
pytest
```

To exercise the live mailbox end-to-end, point the
[MCP Inspector](https://github.com/modelcontextprotocol/inspector) at
`http://localhost:8000/mcp`, complete the OAuth login with your admin password, then
call `list_unread_emails`.

---

## Deploy (public HTTPS required)

Claude must reach the server over **HTTPS on the public internet**, and
`PUBLIC_BASE_URL` must equal that exact origin.

### Docker (portable — Fly.io / Render / Railway / a VPS)

```bash
docker build -t aruba-email-mcp .
docker run -p 8000:8000 \
  -e PUBLIC_BASE_URL="https://mail-mcp.yourdomain.tld" \
  -e ARUBA_EMAIL="you@yourdomain.it" \
  -e ARUBA_PASSWORD="********" \
  -e ADMIN_LOGIN_PASSWORD="********" \
  -v aruba_mcp_data:/data -e DATA_DIR=/data \
  aruba-email-mcp
```

Put it behind the platform's TLS (Fly.io/Render/Railway terminate TLS for you) or a
reverse proxy that does. Example with Caddy on a VPS:

```
mail-mcp.yourdomain.tld {
    reverse_proxy 127.0.0.1:8000
}
```

Keep the `/data` volume so issued OAuth tokens survive restarts.

---

## Add it to Claude

**claude.ai web · desktop · iPhone/Android** — do this once; it then appears on all of them:

1. **Settings → Connectors → Add custom connector**.
2. Paste your `PUBLIC_BASE_URL` (Claude discovers `/mcp` and the OAuth metadata).
3. Complete the OAuth login — enter your **admin password** on the consent screen.
4. Ask Claude: *"Check my inbox for new email."*

**Claude Code (CLI), all projects** — one-time, user-scoped:

```bash
claude mcp add --scope user --transport http aruba-email https://mail-mcp.yourdomain.tld/mcp
```

---

## Security notes

- No secrets in the repo: `.env` and `*.sqlite` are git-ignored; `.env.example`
  holds placeholders only.
- Dynamic client registration is open per the OAuth spec, but the **admin-password
  gate** on `/authorize` protects the mailbox.
- HTTPS is mandatory (OAuth issuer/redirect). Access tokens expire (default 1h) and
  refresh tokens rotate on use.
- Email bodies and credentials are never logged.
