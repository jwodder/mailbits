from datetime import datetime
from email import headerregistry as hr
from email.message import Message
import inspect
import sys
from typing import Any, Callable, Dict, List, Optional
from .misc import message2email, parse_addresses

if sys.version_info[:2] >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class MessageDict(TypedDict):
    unixfrom: Optional[str]
    headers: Dict[str, Any]
    preamble: Optional[str]
    content: Any
    epilogue: Optional[str]


def process_unique_string_header(ush: List[Any]) -> str:
    assert len(ush) == 1
    return str(ush[0])


def process_address(addr: hr.Address) -> Dict[str, str]:
    return {
        "display_name": addr.display_name,
        "address": addr.addr_spec,
    }


def process_addr_headers(ahs: List[Any]) -> List[dict]:
    data: List[dict] = []
    for h in ahs:
        assert isinstance(h, hr.AddressHeader)
        for ag in parse_addresses(h):
            if isinstance(ag, hr.Group):
                data.append(
                    {
                        "group": ag.display_name,
                        "addresses": list(map(process_address, ag.addresses)),
                    }
                )
            else:
                data.append(process_address(ag))
    return data


SKIPPED_CT_PARAMS = {
    "charset",
    "boundary",
}


def process_content_type_headers(
    cths: List[Any], include_all: bool = False
) -> Dict[str, Any]:
    assert len(cths) == 1
    return {
        "content_type": cths[0].content_type,
        "params": {
            k: v
            for k, v in cths[0].params.items()
            if include_all or k not in SKIPPED_CT_PARAMS
        },
    }


def process_date_headers(dh: List[Any]) -> List[datetime]:
    data = []
    for h in dh:
        assert isinstance(h, hr.DateHeader)
        data.append(h.datetime)
    return data


def process_unique_date_header(dh: List[Any]) -> datetime:
    assert len(dh) == 1
    assert isinstance(dh[0], hr.UniqueDateHeader)
    return dh[0].datetime


def process_unique_single_addr_header(ah: List[Any]) -> Dict[str, str]:
    assert len(ah) == 1
    assert isinstance(ah[0], hr.UniqueSingleAddressHeader)
    return process_address(ah[0].address)


def process_single_addr_header(ah: List[Any]) -> List[Dict[str, str]]:
    data = []
    for h in ah:
        assert isinstance(h, hr.SingleAddressHeader)
        data.append(process_address(h.address))
    return data


def process_content_disposition_header(cdh: List[Any]) -> Dict[str, Any]:
    assert len(cdh) == 1
    assert isinstance(cdh[0], hr.ContentDispositionHeader)
    return {
        "disposition": cdh[0].content_disposition,
        "params": dict(cdh[0].params),
    }


def process_cte_header(cteh: List[Any]) -> str:
    assert len(cteh) == 1
    assert isinstance(cteh[0], hr.ContentTransferEncodingHeader)
    return cteh[0].cte  # TODO: When is this different from `str(cteh[0])`?


def process_mime_version_header(mvh: List[Any]) -> Optional[str]:
    assert len(mvh) == 1
    assert isinstance(mvh[0], hr.MIMEVersionHeader)
    return mvh[0].version


HEADER_PROCESSORS: Dict[str, Callable] = {
    "subject": process_unique_string_header,
    "message-id": process_unique_string_header,
    "from": process_addr_headers,
    "to": process_addr_headers,
    "cc": process_addr_headers,
    "bcc": process_addr_headers,
    "content-type": process_content_type_headers,
    "date": process_unique_date_header,
    "resent-date": process_date_headers,
    "orig-date": process_unique_date_header,
    "resent-to": process_addr_headers,
    "resent-cc": process_addr_headers,
    "resent-bcc": process_addr_headers,
    "resent-from": process_addr_headers,
    "reply-to": process_addr_headers,
    "sender": process_unique_single_addr_header,
    "resent-sender": process_single_addr_header,
    "content-disposition": process_content_disposition_header,
    "content-transfer-encoding": process_cte_header,
    "mime-version": process_mime_version_header,
}

SKIPPED_HEADERS = {
    "content-transfer-encoding",
    "mime-version",
}


def email2dict(msg: Message, include_all: bool = False) -> "MessageDict":
    """
    Convert a `Message` object to a `dict`.  All encoded text & bytes are
    decoded into their natural values.

    Need to examine a `Message` but find the builtin Python API too fiddly?
    Need to check that a `Message` has the content & structure you expect?
    Need to compare two `Message` instances for equality?  Need to pretty-print
    the structure of a `Message`?  Then `email2dict()` has your back.

    By default, any information specific to how the message is encoded
    (:mailheader:`Content-Type` parameters,
    :mailheader:`Content-Transfer-Encoding`, etc.) is not reported, as the
    focus is on the actual content rather than the choices made in representing
    it.  To include this information anyway, set ``include_all`` to `True`.
    """

    msg = message2email(msg)
    data: MessageDict = {
        "unixfrom": msg.get_unixfrom(),
        "headers": {},
        "preamble": None,
        "content": None,
        "epilogue": None,
    }
    for header in msg.keys():
        header = header.lower()
        if header in SKIPPED_HEADERS and not include_all:
            continue
        values = msg.get_all(header)
        if not values:
            continue
        try:
            processor = HEADER_PROCESSORS[header]
        except KeyError:
            v = list(map(str, values))
        else:
            kwargs = {}
            if takes_argument(processor, "include_all"):
                kwargs["include_all"] = include_all
            v = processor(values, **kwargs)
        data["headers"][header] = v
    data["preamble"] = msg.preamble
    if msg.get_content_maintype() == "message":
        # Some "message/*" subtypes (specifically, as of Python 3.9, rfc822 and
        # external-body, but we should try to be future-proof) have
        # get_content() return a Message, while others return bytes.
        content = msg.get_content()
        if isinstance(content, Message):
            data["content"] = email2dict(content, include_all=include_all)
        else:
            data["content"] = content
    elif msg.is_multipart():
        data["content"] = [
            email2dict(p, include_all=include_all) for p in msg.iter_parts()
        ]
    else:
        data["content"] = msg.get_content()
    data["epilogue"] = msg.epilogue
    return data


def takes_argument(callable_obj: Callable, argname: str) -> bool:
    sig = inspect.signature(callable_obj)
    for param in sig.parameters.values():
        if (
            param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
            and param.name == argname
        ):
            return True
        elif param.kind is param.VAR_KEYWORD:
            return True
    return False
