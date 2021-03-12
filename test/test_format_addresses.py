from email.headerregistry import Address, Group
from typing import List, Union
import pytest
from mailbits import format_addresses


@pytest.mark.parametrize(
    "addresses,fmt",
    [
        ([], ""),
        (["foo@example.com"], "foo@example.com"),
        (["foo@example.com", "bar@example.org"], "foo@example.com, bar@example.org"),
        (
            [Address("Fabian Oo", addr_spec="foo@example.com")],
            "Fabian Oo <foo@example.com>",
        ),
        (
            [
                Address("Fabian Oo", addr_spec="foo@example.com"),
                Address("Bastian Arrr", addr_spec="bar@example.org"),
            ],
            "Fabian Oo <foo@example.com>, Bastian Arrr <bar@example.org>",
        ),
        (
            [Address("Fabian O. Oh", addr_spec="foo@example.com")],
            '"Fabian O. Oh" <foo@example.com>',
        ),
        (
            [Address("Zoë Façade", addr_spec="zoe.facade@naïveté.fr")],
            "Zoë Façade <zoe.facade@naïveté.fr>",
        ),
        (
            [
                Group("undisclosed recipients", ()),
                "luser@example.nil",
                Group(
                    "friends",
                    (
                        Address("", addr_spec="you@there.net"),
                        Address("Thaddeus Hem", addr_spec="them@hither.yon"),
                    ),
                ),
            ],
            "undisclosed recipients:;, luser@example.nil,"
            " friends: you@there.net, Thaddeus Hem <them@hither.yon>;",
        ),
    ],
)
def test_format_addresses(
    addresses: List[Union[str, Address, Group]], fmt: str
) -> None:
    assert format_addresses(addresses) == fmt
