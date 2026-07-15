"""Offline tests for MIME building / reply threading (no network)."""

from email.message import EmailMessage

from aruba_email_mcp import mailbuild


def test_build_message_text_and_html():
    msg = mailbuild.build_message(
        sender="carlo@potential.contractors",
        to=["a@b.com", "c@d.com"],
        subject="Ciao",
        body_text="Testo",
        body_html="<p>Testo</p>",
        cc=["e@f.com"],
        domain="potential.contractors",
    )
    assert msg["From"] == "carlo@potential.contractors"
    assert msg["To"] == "a@b.com, c@d.com"
    assert msg["Cc"] == "e@f.com"
    assert msg["Subject"] == "Ciao"
    assert msg["Message-ID"] and "potential.contractors" in msg["Message-ID"]
    assert msg.is_multipart()  # text + html alternative


def test_build_reply_threading_and_subject():
    original = EmailMessage()
    original["From"] = "Andrea <andrea@example.it>"
    original["To"] = "carlo@potential.contractors"
    original["Subject"] = "Pranzo"
    original["Message-ID"] = "<orig-123@example.it>"
    original["References"] = "<older-1@example.it>"
    original.set_content("Ci vediamo lunedì?")

    reply = mailbuild.build_reply(
        original=original,
        sender="carlo@potential.contractors",
        body_text="Sì, perfetto.",
        domain="potential.contractors",
    )

    assert reply["Subject"] == "Re: Pranzo"
    assert reply["To"] == "Andrea <andrea@example.it>"
    assert reply["In-Reply-To"] == "<orig-123@example.it>"
    # References must chain the old references + original message-id.
    assert "<older-1@example.it>" in reply["References"]
    assert "<orig-123@example.it>" in reply["References"]
    body = reply.get_body(preferencelist=("plain",)).get_content()
    assert "Sì, perfetto." in body
    assert "> Ci vediamo lunedì?" in body  # quoted original


def test_build_reply_no_double_re_prefix():
    original = EmailMessage()
    original["From"] = "x@y.com"
    original["Subject"] = "Re: già risposta"
    original.set_content("hi")
    reply = mailbuild.build_reply(
        original=original, sender="me@z.com", body_text="ok"
    )
    assert reply["Subject"] == "Re: già risposta"
