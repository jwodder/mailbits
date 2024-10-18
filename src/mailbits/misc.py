from __future__ import annotations
from collections.abc import Iterable
import email
from email import headerregistry as hr
from email import policy
from email.generator import BytesGenerator
from email.headerregistry import Address, Group
from email.message import EmailMessage, Message
from io import BytesIO
from mailbox import MMDFMessage, mboxMessage
from typing import Any, Union
import attr

AddressOrGroup = Union[str, Address, Group]

# <https://github.com/python/typeshed/issues/12852>
ENCODED_POLICY = policy.default.clone(utf8=False, max_line_length=0)  # type: ignore[call-arg]


@attr.s(auto_attribs=True)
class ContentType:
    """
    The `ContentType` class provides a representation of a parsed Content-Type
    header value.  Parse Content-Type strings with the `parse()` classmethod,
    inspect the parts via the `content_type`, `maintype`, `subtype`, and
    `params` attributes (the last three of which can be mutated), convert back
    to a string with `str()`, and convert to ASCII bytes using encoded words
    for non-ASCII with `bytes()`.
    """

    maintype: str
    subtype: str
    params: dict[str, str] = attr.ib(factory=dict)

    @classmethod
    def parse(cls, s: str) -> ContentType:
        """Parse a :mailheader:`Content-Type` string"""
        ct = parse_header("Content-Type", s)
        assert isinstance(ct, hr.ContentTypeHeader)
        return cls(ct.maintype, ct.subtype, dict(ct.params))

    @property
    def content_type(self) -> str:
        """A string of the form "maintype/subtype" """
        return f"{self.maintype}/{self.subtype}"

    def __str__(self) -> str:
        ct = self.content_type
        msg = EmailMessage()
        msg["Content-Type"] = ct
        if msg["Content-Type"].defects:
            raise ValueError(ct)
        for k, v in self.params.items():
            msg.set_param(k, v)
        return str(msg["Content-Type"])

    def __bytes__(self) -> bytes:
        ct = self.content_type
        msg = EmailMessage()
        msg["Content-Type"] = ct
        if msg["Content-Type"].defects:
            raise ValueError(ct)
        for k, v in self.params.items():
            msg.set_param(k, v)
        b = policy.default.fold_binary("Content-Type", msg["Content-Type"])
        prefix = b"Content-Type: "
        assert b.startswith(prefix)
        return b[len(prefix) :].rstrip(b"\n")


def format_addresses(addresses: Iterable[AddressOrGroup], encode: bool = False) -> str:
    """
    Convert an iterable of e-mail address strings (of the form
    "``foo@example.com``", without angle brackets or a display name),
    `~email.headerregistry.Address` objects, and/or
    `~email.headerregistry.Group` objects into a formatted string.  If
    ``encode`` is `False` (the default), non-ASCII characters are left as-is.
    If it is `True`, non-ASCII display names are converted into :RFC:`2047`
    encoded words, and non-ASCII domain names are encoded using Punycode.
    """
    addrs = []
    for a in addresses:
        if isinstance(a, str):
            a = Address(addr_spec=a)
        if encode:
            if isinstance(a, Address):
                a = idna_address(a)
            else:
                assert isinstance(a, Group)
                a = Group(a.display_name, tuple(map(idna_address, a.addresses)))
        addrs.append(a)
    msg = EmailMessage()
    msg["To"] = addrs
    if encode:
        folded = msg["To"].fold(policy=ENCODED_POLICY)
        assert isinstance(folded, str)
        if folded == "To:\n":
            return ""
        prefix = "To: "
        assert folded.startswith(prefix)
        return folded[len(prefix) :].rstrip("\n")
    else:
        return str(msg["To"])


def parse_address(s: str) -> Address:
    """
    Parse a single e-mail address — either a raw address like
    "``foo@example.com``" or a combined display name & address like "``Fabian
    Oh <foo@example.com>``" into an `Address` object.
    """
    h = parse_header("Sender", s)
    assert isinstance(h, hr.SingleAddressHeader)
    return h.address


def parse_addresses(s: str | hr.AddressHeader) -> list[Address | Group]:
    """
    Parse a formatted list of e-mail addresses or the contents of an
    `EmailMessage`'s "To", "CC", "BCC", etc. header into a list of `Address`
    and/or `Group` objects.
    """
    if isinstance(s, str):
        h = parse_header("To", s)
        assert isinstance(h, hr.AddressHeader)
    else:
        h = s
    parsed: list[Address | Group] = []
    for g in h.groups:
        if g.display_name is not None:
            parsed.append(g)
        else:
            parsed.extend(g.addresses)
    return parsed


def recipient_addresses(msg: EmailMessage) -> list[str]:
    """
    Return a sorted list of all of the distinct e-mail addresses (not including
    display names) in an `EmailMessage`'s combined "To", "CC", and "BCC"
    headers.
    """
    recipients = set()
    for key in ["To", "CC", "BCC"]:
        for header in msg.get_all(key, []):
            assert isinstance(header, hr.AddressHeader)
            for addr in header.addresses:
                recipients.add(addr.addr_spec)
    return sorted(recipients)


def message2email(msg: Message) -> EmailMessage:
    """
    Convert an instance of the old `Message` class (or one of its subclasses,
    like a `mailbox` message class) to an instance of the new `EmailMessage`
    class with the ``default`` policy.  If ``msg`` is already an
    `EmailMessage`, it is returned unchanged.
    """
    if isinstance(msg, EmailMessage):
        return msg
    # Message.as_bytes() refolds long header lines (which can result in changes
    # in whitespace after reparsing) and doesn't give a way to change this, so
    # we need to use a BytesGenerator manually.
    fp = BytesIO()
    # TODO: Instead of maxheaderlen, use a policy with refold_source=None?
    g = BytesGenerator(fp, mangle_from_=False, maxheaderlen=0)
    g.flatten(msg, unixfrom=msg.get_unixfrom() is not None)
    fp.seek(0)
    emsg = email.message_from_binary_file(fp, policy=policy.default)
    assert isinstance(emsg, EmailMessage)
    # MMDFMessage and mboxMessage make their "From " lines available though a
    # different method than normal Messages, so we have to copy it over
    # manually.
    if isinstance(msg, (MMDFMessage, mboxMessage)):
        emsg.set_unixfrom("From " + msg.get_from())
    return emsg


def parse_header(name: str, value: str) -> Any:
    # mypy fails on the next line because of
    # <https://github.com/python/mypy/issues/10131>
    h = policy.default.header_factory(name, value)  # type: ignore
    assert isinstance(h, hr.BaseHeader)
    if h.defects:
        # You'd think the strict policy would raise an error on defective
        # headers, but no...
        raise ValueError(value)
    return h


def idna_address(addr: Address) -> Address:
    return Address(
        display_name=addr.display_name,
        username=addr.username,
        domain=addr.domain.encode("idna").decode("us-ascii"),
    )
