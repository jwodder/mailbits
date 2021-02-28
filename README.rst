.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://github.com/jwodder/email2dict/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/email2dict/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/email2dict/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/email2dict

.. image:: https://img.shields.io/github/license/jwodder/email2dict.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/email2dict>`_
| `Issues <https://github.com/jwodder/email2dict/issues>`_

``email2dict`` converts Python ``Message`` & ``EmailMessage`` instances into
structured ``dict``\s.  Need to examine a ``Message`` but find the builtin
Python API too fiddly?  Need to check that a ``Message`` has the content &
structure you expect?  Need to compare two ``Message`` instances for equality?
Need to pretty-print the structure of a ``Message``?  Then ``email2dict`` has
your back.


Installation
============
``email2dict`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install it::

    python3 -m pip install git+https://github.com/jwodder/email2dict


Example
=======

The ``email`` `examples page`__ in the Python docs includes an example of
constructing an HTML e-mail with an alternative plain text version (It's the
one with the subject "Ayons asperges pour le déjeuner").  Passing the resulting
``EmailMessage`` object to the ``email2dict()`` function produces the following
output structure:

__ https://docs.python.org/3/library/email.examples.html

.. code:: python

    {
        "headers": {
            "subject": "Ayons asperges pour le déjeuner",
            "from": [
                {
                    "realname": "Pepé Le Pew",
                    "address": "pepe@example.com",
                },
            ],
            "to": [
                {
                    "realname": "Penelope Pussycat",
                    "address": "penelope@example.com",
                },
                {
                    "realname": "Fabrette Pussycat",
                    "address": "fabrette@example.com",
                },
            ],
            "content-type": "multipart/alternative",
        },
        "preamble": None,
        "content": [
            {
                "headers": {
                    "content-type": "text/plain"
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
                "headers": {
                    "content-type": "multipart/related",
                },
                "preamble": None,
                "content": [
                    {
                        "headers": {
                            "content-type": "text/html",
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
                        "headers": {
                            "content-type": "image/png",
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


API
===

The ``email2dict`` module provides a single function, also named ``email2dict``:

.. code:: python

    email2dict(msg: email.message.Message) -> Dict[str, Any]

Convert a ``Message`` object to a ``dict`` with the following fields:

``headers``
    A ``dict`` mapping lowercased header field names to values.  The following
    headers have special representations:

    ``subject``
        A single string

    ``from``, ``to``, ``cc``, ``bcc``, ``resent-from``, ``resent-to``, ``resent-cc``, ``resent-bcc``, ``reply-to``
        A list of groups and/or addresses.  Addresses are represented as
        ``dict``\s with two string fields: ``realname`` (an empty string if not
        given) and ``address``.  Groups are represented as ``dict``\s with a
        ``group`` field giving the name of the group and an ``addresses`` field
        giving a list of addresses in the group.

    ``message-id``
        A single string

    ``content-type``
        A string of the form ``maintype/subtype`` (e.g., "text/plain")

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
        Discarded; see below

    ``mime-version``
        Discarded; see below

    All other headers are represented as lists of strings.

``preamble``
    The message's preamble__

    __ https://docs.python.org/3/library/email.message.html
       #email.message.EmailMessage.preamble

``content``
    If the message is multipart, this is a list of message ``dict``\s,
    structured the same way as the top-level ``dict``.  If the message's
    Content-Type is ``text/*``, this is a ``str`` giving the contents of the
    message.  Otherwise, it is a ``bytes`` giving the contents of the message.

``epilogue``
    The message's epilogue__

    __ https://docs.python.org/3/library/email.message.html
       #email.message.EmailMessage.epilogue

Note that any information specific to how the message is encoded (Content-Type
parameters, Content-Transfer-Encoding, etc.) is not reported, as the focus is
on the actual content rather than the choices made in representing it.