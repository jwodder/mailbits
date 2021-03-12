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
    with pytest.raises(ValueError) as excinfo:
        parse_address(s)
    assert str(excinfo.value) == s
