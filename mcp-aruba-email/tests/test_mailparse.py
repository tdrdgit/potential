"""Offline tests for the email-parsing helpers (no network)."""

from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default as default_policy

from aruba_email_mcp import mailparse


def _sample_message() -> bytes:
    msg = EmailMessage()
    msg["From"] = "Andrea Bonanomi <andrea@example.it>"
    msg["To"] = "carlo@potential.contractors"
    # RFC 2047 encoded-word subject (UTF-8 with accents).
    msg["Subject"] = "=?utf-8?b?UHJhbnpvIGNvbiBjYWbDqA==?="  # "Pranzo con cafè"
    msg["Date"] = "Mon, 13 Jul 2026 15:05:17 +0000"
    msg.set_content("Ciao Carlo,\nconfermo il pranzo.\nA presto")
    msg.add_alternative(
        "<html><body><style>.x{color:red}</style><p>Ciao <b>Carlo</b>, confermo.</p></body></html>",
        subtype="html",
    )
    msg.add_attachment(
        b"%PDF-1.4 fake",
        maintype="application",
        subtype="pdf",
        filename="agenda.pdf",
    )
    return msg.as_bytes()


def _parsed():
    return BytesParser(policy=default_policy).parsebytes(_sample_message())


def test_decode_mime_header():
    assert mailparse.decode_mime_header("=?utf-8?b?UHJhbnpvIGNvbiBjYWbDqA==?=") == "Pranzo con cafè"
    assert mailparse.decode_mime_header(None) == ""


def test_format_addresses():
    addrs = mailparse.format_addresses("Andrea Bonanomi <andrea@example.it>, x@y.com")
    assert addrs == ["Andrea Bonanomi <andrea@example.it>", "x@y.com"]


def test_parse_date_iso():
    iso = mailparse.parse_date("Mon, 13 Jul 2026 15:05:17 +0000")
    assert iso.startswith("2026-07-13T15:05:17")


def test_extract_bodies_and_snippet():
    msg = _parsed()
    text, html = mailparse.extract_bodies(msg)
    assert "confermo il pranzo" in text
    assert "<b>Carlo</b>" in html
    snippet = mailparse.make_snippet(msg)
    assert "confermo il pranzo" in snippet
    # Snippet should never contain raw HTML tags.
    assert "<" not in snippet


def test_html_to_text_strips_style_and_tags():
    out = mailparse.html_to_text("<style>.x{color:red}</style><p>Hello <b>World</b></p>")
    assert "color:red" not in out
    assert out == "Hello World"


def test_list_attachments():
    atts = mailparse.list_attachments(_parsed())
    assert len(atts) == 1
    assert atts[0]["filename"] == "agenda.pdf"
    assert atts[0]["content_type"] == "application/pdf"
    assert atts[0]["size"] > 0
