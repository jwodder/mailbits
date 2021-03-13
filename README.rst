.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/mailbits/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/mailbits/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/mailbits/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/mailbits

.. image:: https://img.shields.io/pypi/pyversions/mailbits.svg
    :target: https://pypi.org/project/mailbits/

.. image:: https://img.shields.io/github/license/jwodder/mailbits.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/mailbits>`_
| `PyPI <https://pypi.org/project/mailbits/>`_
| `Issues <https://github.com/jwodder/mailbits/issues>`_
| `Changelog <https://github.com/jwodder/mailbits/blob/master/CHANGELOG.md>`_

``mailbits`` provides a small assortment of functions for working with the
Python standard library's ``Message``/``EmailMessage``, ``Address``, and
``Group`` types, as well as a couple other features.  It can parse & reassemble
Content-Type strings, convert instances of the old ``Message`` class to the new
``EmailMessage``, convert ``Message`` & ``EmailMessage`` instances into
structured ``dict``\s, parse addresses, format address lists, and extract
recipients' raw e-mail addresses from an ``EmailMessage``.


Installation
============
``mailbits`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install it::

    python3 -m pip install mailbits


API
===

``ContentType``
---------------

The ``ContentType`` class provides a representation of a parsed Content-Type
header value.  Parse Content-Type strings with the ``parse()`` classmethod,
inspect the parts via the ``content_type``, ``maintype``, ``subtype``, and
``params`` attributes (the last three of which can be mutated), convert back to
a string with ``str()``, and convert to ASCII bytes using encoded words for
non-ASCII with ``bytes()``.

>>> from mailbits import ContentType
>>> ct = ContentType.parse("text/plain; charset=utf-8; name*=utf-8''r%C3%A9sum%C3%A9.txt")
>>> ct
ContentType(maintype='text', subtype='plain', params={'charset': 'utf-8', 'name': 'résumé.txt'})
>>> ct.content_type
'text/plain'
>>> str(ct)
'text/plain; charset="utf-8"; name="résumé.txt"'
>>> bytes(ct)
b'text/plain; charset="utf-8"; name*=utf-8\'\'r%C3%A9sum%C3%A9.txt'


``email2dict()``
----------------

.. code:: python

    class MessageDict(TypedDict):
        unixfrom: Optional[str]
        headers: Dict[str, Any]
        preamble: Optional[str]
        content: Any
        epilogue: Optional[str]

    mailbits.email2dict(msg: email.message.Message, include_all: bool = False) -> MessageDict

Convert a ``Message`` object to a ``dict``.  All encoded text & bytes are
decoded into their natural values.

Need to examine a ``Message`` but find the builtin Python API too fiddly?  Need
to check that a ``Message`` has the content & structure you expect?  Need to
compare two ``Message`` instances for equality?  Need to pretty-print the
structure of a ``Message``?  Then ``email2dict()`` has your back.

By default, any information specific to how the message is encoded (Content-Type
parameters, Content-Transfer-Encoding, etc.) is not reported, as the focus is
on the actual content rather than the choices made in representing it.  To
include this information anyway, set ``include_all`` to ``True``.

The output structure has the following fields:

``unixfrom``
    The "From " line marking the start of the message in a mbox, if any

``headers``
    A ``dict`` mapping lowercased header field names to values.  The following
    headers have special representations:

    ``subject``
        A single string

    ``from``, ``to``, ``cc``, ``bcc``, ``resent-from``, ``resent-to``, ``resent-cc``, ``resent-bcc``, ``reply-to``
        A list of groups and/or addresses.  Addresses are represented as
        ``dict``\s with two string fields: ``display_name`` (an empty string if
        not given) and ``address``.  Groups are represented as ``dict``\s with
        a ``group`` field giving the name of the group and an ``addresses``
        field giving a list of addresses in the group.

    ``message-id``
        A single string

    ``content-type``
        A ``dict`` containing a ``content_type`` field (a string of the form
        ``maintype/subtype``, e.g., ``"text/plain"``) and a ``params`` field (a
        ``dict`` of string keys & values).  The ``charset`` and ``boundary``
        parameters are discarded unless ``include_all`` is ``True``.

    ``date``
        A ``datetime.datetime`` instance

    ``orig-date``
        A ``datetime.datetime`` instance

    ``resent-date``
        A list of ``datetime.datetime`` instances

    ``sender``
        A single address ``dict``

    ``resent-sender``
        A list of address ``dict``\s

    ``content-disposition``
        A ``dict`` containing a ``disposition`` field (value either
        ``"inline"`` or ``"attachment"``) and a ``params`` field (a ``dict`` of
        string keys & values)

    ``content-transfer-encoding``
        A single string.  This header is discarded unless ``include_all`` is
        ``True``.

    ``mime-version``
        A single string.  This header is discarded unless ``include_all`` is
        ``True``.

    All other headers are represented as lists of strings.

``preamble``
    The message's preamble__

    __ https://docs.python.org/3/library/email.message.html
       #email.message.EmailMessage.preamble

``content``
    If the message is multipart, this is a list of message ``dict``\s,
    structured the same way as the top-level ``dict``.  If the message's
    Content-Type is ``message/rfc822`` or ``message/external-body``, this is a
    single message ``dict``.  If the message's Content-Type is ``text/*``, this
    is a ``str`` giving the contents of the message.  Otherwise, it is a
    ``bytes`` giving the contents of the message.

``epilogue``
    The message's epilogue__

    __ https://docs.python.org/3/library/email.message.html
       #email.message.EmailMessage.epilogue

An example: The ``email`` `examples page`__ in the Python docs includes an
example of constructing an HTML e-mail with an alternative plain text version
(It's the one with the subject "Ayons asperges pour le déjeuner").  Passing the
resulting ``EmailMessage`` object to ``email2dict()`` produces the following
output structure:

__ https://docs.python.org/3/library/email.examples.html

.. code:: python

    {
        "unixfrom": None,
        "headers": {
            "subject": "Ayons asperges pour le déjeuner",
            "from": [
                {
                    "display_name": "Pepé Le Pew",
                    "address": "pepe@example.com",
                },
            ],
            "to": [
                {
                    "display_name": "Penelope Pussycat",
                    "address": "penelope@example.com",
                },
                {
                    "display_name": "Fabrette Pussycat",
                    "address": "fabrette@example.com",
                },
            ],
            "content-type": {
                "content_type": "multipart/alternative",
                "params": {},
            },
        },
        "preamble": None,
        "content": [
            {
                "unixfrom": None,
                "headers": {
                    "content-type": {
                        "content_type": "text/plain",
                        "params": {},
                    },
                },
                "preamble": None,
                "content": (
                    "Salut!\n"
                    "\n"
                    "Cela ressemble à un excellent recipie[1] déjeuner.\n"
                    "\n"
                    "[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718\n"
                    "\n"
                    "--Pepé\n"
                ),
                "epilogue": None,
            },
            {
                "unixfrom": None,
                "headers": {
                    "content-type": {
                        "content_type": "multipart/related",
                        "params": {},
                    },
                },
                "preamble": None,
                "content": [
                    {
                        "unixfrom": None,
                        "headers": {
                            "content-type": {
                                "content_type": "text/html",
                                "params": {},
                            },
                        },
                        "preamble": None,
                        "content": (
                            "<html>\n"
                            "  <head></head>\n"
                            "  <body>\n"
                            "    <p>Salut!</p>\n"
                            "    <p>Cela ressemble à un excellent\n"
                            "        <a href=\"http://www.yummly.com/recipe/Roasted-Asparagus-"
                            "Epicurious-203718\">\n"
                            "            recipie\n"
                            "        </a> déjeuner.\n"
                            "    </p>\n"
                            "    <img src=\"cid:RANDOM_MESSAGE_ID\" />\n"
                            "  </body>\n"
                            "</html>\n"
                        ),
                        "epilogue": None,
                    },
                    {
                        "unixfrom": None,
                        "headers": {
                            "content-type": {
                                "content_type": "image/png",
                                "params": {},
                            },
                            "content-disposition": {
                                "disposition": "inline",
                                "params": {},
                            },
                            "content-id": ["<RANDOM_MESSAGE_ID>"],
                        },
                        "preamble": None,
                        "content": b'IMAGE BLOB',
                        "epilogue": None,
                    },
                ],
                "epilogue": None,
            },
        ],
        "epilogue": None,
    }


``format_addresses()``
----------------------

.. code:: python

    mailbits.format_addresses(addresses: Iterable[Union[str, Address, Group]], encode: bool = False) -> str

Convert an iterable of e-mail address strings (of the form
"``foo@example.com``", without angle brackets or a display name),
``email.headerregistry.Address`` objects, and/or ``email.headerregistry.Group``
objects into a formatted string.  If ``encode`` is ``False`` (the default),
non-ASCII characters are left as-is.  If it is ``True``, non-ASCII display
names are converted into :RFC:`2047` encoded words, and non-ASCII domain names
are encoded using Punycode.


``message2email()``
-------------------

.. code:: python

    mailbits.message2email(msg: email.message.Message) -> email.message.EmailMessage

Convert an instance of the old ``Message`` class (or one of its subclasses,
like a ``mailbox`` message class) to an instance of the new ``EmailMessage``
class with the ``default`` policy.  If ``msg`` is already an ``EmailMessage``,
it is returned unchanged.


``parse_address()``
-------------------

.. code:: python

    mailbits.parse_address(s: str) -> email.headerregistry.Address

Parse a single e-mail address — either a raw address like "``foo@example.com``"
or a combined display name & address like "``Fabian Oh <foo@example.com>``"
into an ``Address`` object.


``parse_addresses()``
---------------------

.. code:: python

    mailbits.parse_addresses(s: Union[str, email.headerregistry.AddressHeader]) \
        -> List[Union[email.headerregistry.Address, email.headerregistry.Group]]

Parse a formatted list of e-mail addresses or the contents of an
``EmailMessage``'s "To", "CC", "BCC", etc. header into a list of ``Address``
and/or ``Group`` objects.


``recipient_addresses()``
-------------------------

.. code:: python

    mailbits.recipient_addresses(msg: email.message.EmailMessage) -> List[str]

Return a sorted list of all of the distinct e-mail addresses (not including
display names) in an ``EmailMessage``'s combined "To", "CC", and "BCC" headers.
