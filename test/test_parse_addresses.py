from __future__ import annotations
from email.headerregistry import Address, Group
import pytest
from mailbits import parse_addresses


@pytest.mark.parametrize(
    "s,addresses",
    [
        ("", []),
        (
            "Some User <luser@example.nil>",
            [Address("Some User", addr_spec="luser@example.nil")],
        ),
        (
            "Some User <luser@example.nil>, extra@somewhere.there",
            [
                Address("Some User", addr_spec="luser@example.nil"),
                Address(addr_spec="extra@somewhere.there"),
            ],
        ),
        (
            (
                "friends: luser@example.nil, extra@somewhere.there;,"
                " enemies:loozr@eggsample.null, surplus@nowhere.here;"
            ),
            [
                Group(
                    "friends",
                    (
                        Address(addr_spec="luser@example.nil"),
                        Address(addr_spec="extra@somewhere.there"),
                    ),
                ),
                Group(
                    "enemies",
                    (
                        Address(addr_spec="loozr@eggsample.null"),
                        Address(addr_spec="surplus@nowhere.here"),
                    ),
                ),
            ],
        ),
        (
            "Zoë Façade <zoe.facade@naïveté.fr>",
            [Address("Zoë Façade", addr_spec="zoe.facade@naïveté.fr")],
        ),
        (
            "=?ISO-8859-1?Q?Keld_J=F8rn_Simonsen?= <keld@dkuug.dk>",
            [Address("Keld Jørn Simonsen", addr_spec="keld@dkuug.dk")],
        ),
    ],
)
def test_parse_addresses(s: str, addresses: list[Address | Group]) -> None:
    assert parse_addresses(s) == addresses
