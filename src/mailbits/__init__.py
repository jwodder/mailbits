"""
Assorted e-mail utility functions

``mailbits`` provides a small assortment of functions for working with the
Python standard library's ``Message``/``EmailMessage``, ``Address``, and
``Group`` types, as well as a couple other features.  It can parse & reassemble
Content-Type strings, convert instances of the old ``Message`` class to the new
``EmailMessage``, convert ``Message`` & ``EmailMessage`` instances into
structured ``dict``\\s, parse addresses, format address lists, and extract
recipients' raw e-mail addresses from an ``EmailMessage``.

Visit <https://github.com/jwodder/mailbits> for more information.
"""

__version__ = "0.2.1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "mailbits@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/mailbits"

from .email2dict import MessageDict, email2dict
from .misc import (
    ContentType,
    format_addresses,
    message2email,
    parse_address,
    parse_addresses,
    recipient_addresses,
)

__all__ = [
    "ContentType",
    "MessageDict",
    "email2dict",
    "format_addresses",
    "message2email",
    "parse_address",
    "parse_addresses",
    "recipient_addresses",
]
