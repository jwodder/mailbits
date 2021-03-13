"""
Assorted e-mail utility functions

``mailbits`` converts Python ``Message`` & ``EmailMessage`` instances into
structured ``dict``\\s.  Need to examine a ``Message`` but find the builtin
Python API too fiddly?  Need to check that a ``Message`` has the content &
structure you expect?  Need to compare two ``Message`` instances for equality?
Need to pretty-print the structure of a ``Message``?  Then ``mailbits`` has
your back.

Visit <https://github.com/jwodder/mailbits> for more information.
"""

__version__ = "0.2.0.dev1"
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
