from email.headerregistry import Address, Group
import sys
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
        (
            [
                Address(
                    "John Jacob Jingleheimer Smith",
                    addr_spec="john.jacob.jingleheimer.smith@his-name-is-my-name-too.com",
                ),
                Address(
                    "Jebediah Obadiah Zachariah Jedediah Springfield",
                    addr_spec="jebediah.obadiah.zachariah.jedediah.springfield@simpsons.state",
                ),
            ],
            "John Jacob Jingleheimer Smith <john.jacob.jingleheimer.smith@his-name-is-my-name-too.com>, Jebediah Obadiah Zachariah Jedediah Springfield <jebediah.obadiah.zachariah.jedediah.springfield@simpsons.state>",
        ),
    ],
)
def test_format_addresses(
    addresses: List[Union[str, Address, Group]], fmt: str
) -> None:
    assert format_addresses(addresses) == fmt


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
            [Address("Zoe Facade", addr_spec="zoe.facade@naïveté.fr")],
            "Zoe Facade <zoe.facade@xn--navet-fsa2b.fr>",
        ),
        pytest.param(
            [Address("Zoë Façade", addr_spec="zoe.facade@naïveté.fr")],
            "=?utf-8?q?Zo=C3=AB_Fa=C3=A7ade?= <zoe.facade@xn--navet-fsa2b.fr>",
            marks=pytest.mark.xfail(
                sys.version_info[:2] < (3, 7),
                reason="Cannot encode non-ASCII display names on pre-Python 3.7",
            ),
        ),
        (
            [
                Group(
                    "internationalized",
                    (
                        Address("Zoe Facade", addr_spec="zoe.facade@naïveté.fr"),
                        Address(addr_spec="wong@example.珠宝"),
                    ),
                ),
            ],
            "internationalized: Zoe Facade <zoe.facade@xn--navet-fsa2b.fr>, wong@example.xn--pbt977c;",
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
        (
            [
                Address(
                    "John Jacob Jingleheimer Smith",
                    addr_spec="john.jacob.jingleheimer.smith@his-name-is-my-name-too.com",
                ),
                Address(
                    "Jebediah Obadiah Zachariah Jedediah Springfield",
                    addr_spec="jebediah.obadiah.zachariah.jedediah.springfield@simpsons.state",
                ),
            ],
            "John Jacob Jingleheimer Smith <john.jacob.jingleheimer.smith@his-name-is-my-name-too.com>, Jebediah Obadiah Zachariah Jedediah Springfield <jebediah.obadiah.zachariah.jedediah.springfield@simpsons.state>",
        ),
    ],
)
def test_format_addresses_encode(
    addresses: List[Union[str, Address, Group]], fmt: str
) -> None:
    assert format_addresses(addresses, encode=True) == fmt
