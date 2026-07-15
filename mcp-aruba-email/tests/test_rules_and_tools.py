"""Tests for the bundled rules file and the full tool set."""

import os

import pytest

from aruba_email_mcp import server


def test_rules_file_loads_and_has_projects():
    rules = server.EMAIL_RULES
    assert rules.strip(), "email_rules.md should be bundled and non-empty"
    for project in ("Mountain Retreat", "Blue Lagoon", "Trenitalia"):
        assert project in rules
    assert "Recap email" in rules


def test_instructions_mention_recap_and_rules():
    assert "get_email_rules" in server.INSTRUCTIONS
    assert "Recap email" in server.INSTRUCTIONS


@pytest.fixture(scope="module")
def mcp_server(tmp_path_factory):
    os.environ.update(
        {
            "PUBLIC_BASE_URL": "https://mail-mcp.test.example",
            "ARUBA_EMAIL": "carlo@carlocasagrande.com",
            "ARUBA_PASSWORD": "x",
            "ADMIN_LOGIN_PASSWORD": "pw",
            "OAUTH_SIGNING_KEY": "k",
            "DATA_DIR": str(tmp_path_factory.mktemp("data")),
        }
    )
    from aruba_email_mcp.config import get_settings

    get_settings.cache_clear()
    return server.build_mcp()


async def test_all_tools_registered(mcp_server):
    names = {t.name for t in await mcp_server.list_tools()}
    assert names == {
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
    }


@pytest.fixture
def anyio_backend():
    return "asyncio"
