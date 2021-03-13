from email.headerregistry import Address
import pytest
from mailbits import parse_address


@pytest.mark.parametrize(
    "s,addr",
    [
        ("person@example.com", Address("", addr_spec="person@example.com")),
        ("<person@example.com>", Address("", addr_spec="person@example.com")),
        (
            "Linus User <person@example.com>",
            Address("Linus User", addr_spec="person@example.com"),
        ),
        (
            '"Linus User" <person@example.com>',
            Address("Linus User", addr_spec="person@example.com"),
        ),
        (
            "Zoë Façade <zoe.facade@naïveté.fr>",
            Address("Zoë Façade", addr_spec="zoe.facade@naïveté.fr"),
        ),
        (
            "=?ISO-8859-1?Q?Keld_J=F8rn_Simonsen?= <keld@dkuug.dk>",
            Address("Keld Jørn Simonsen", addr_spec="keld@dkuug.dk"),
        ),
    ],
)
def test_parse_address(s: str, addr: Address) -> None:
    assert parse_address(s) == addr


@pytest.mark.parametrize(
    "s",
    [
        "",
        "person",
        "Me <person>",
        "Me person",
        "@example.com",
        "<@example.com>",
        "Me <@example.com>",
        "person@example.com, foo@bar.org",
        "Me",
        "person@example.com foo@bar.org",
    ],
)
def test_parse_address_error(s: str) -> None:
    with pytest.raises(ValueError):
        parse_address(s)
