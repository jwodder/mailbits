from __future__ import annotations
from email.message import EmailMessage
import pytest
from mailbits import recipient_addresses


@pytest.mark.parametrize(
    "headers,addresses",
    [
        ({}, []),
        (
            {"To": "Some User <luser@example.nil>"},
            ["luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>",
                "From": "not-listed@nowhere.nil",
            },
            ["luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>, extra@somewhere.there",
            },
            ["extra@somewhere.there", "luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>",
                "CC": "extra@somewhere.there",
            },
            ["extra@somewhere.there", "luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>",
                "CC": "Some User Again <luser@example.nil>",
            },
            ["luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>",
                "BCC": "extra@somewhere.there",
            },
            ["extra@somewhere.there", "luser@example.nil"],
        ),
        (
            {
                "To": "Some User <luser@example.nil>",
                "CC": "extra@somewhere.there",
                "BCC": "surplus@nowhere.here",
            },
            ["extra@somewhere.there", "luser@example.nil", "surplus@nowhere.here"],
        ),
        (
            {
                "To": (
                    "friends: luser@example.nil, extra@somewhere.there;,"
                    " enemies:loozr@eggsample.null, surplus@nowhere.here;"
                ),
            },
            [
                "extra@somewhere.there",
                "loozr@eggsample.null",
                "luser@example.nil",
                "surplus@nowhere.here",
            ],
        ),
    ],
)
def test_recipient_addresses(headers: dict[str, str], addresses: list[str]) -> None:
    msg = EmailMessage()
    for k, v in headers.items():
        msg[k] = v
    assert recipient_addresses(msg) == addresses
