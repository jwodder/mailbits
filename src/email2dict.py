"""
Convert EmailMessage objects to dicts

Visit <https://github.com/jwodder/email2dict> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'email2dict@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/email2dict'

import email
from email import policy
from email.message import EmailMessage, Message

def process_address(addr):
    return {
        "realname": addr.display_name,
        "address": addr.addr_spec,
    }

def process_addr_headers(ahs):
    data = []
    for h in ahs:
        for g in h.groups:
            if g.display_name is not None:
                group = {"group": g.display_name, "addresses": []}
                data.append(group)
                addrlist = group["addresses"]
            else:
                addrlist = data
            addrlist.extend(map(process_address, g.addresses))
    return data

def process_content_type_headers(cths):
    # Discard params
    ### TODO: Filter out certain params instead?
    assert len(cths) == 1
    return cths[0].content_type

def process_date_headers(dh):
    return [h.datetime for h in dh]

def process_unique_date_header(dh):
    assert len(dh) == 1
    return dh[0].datetime

def process_unique_single_addr_header(ah):
    assert len(ah) == 1
    return process_address(ah[0].address)

def process_single_addr_header(ah):
    return [process_address(h.address) for h in ah]

def process_content_disposition_header(cdh):
    assert len(cdh) == 1
    data = {
        "disposition": cdh[0].content_disposition
    }
    if cdh[0].params:
        data["params"] = dict(cdh[0].params)
    return data

HEADER_PROCESSORS = {
    # "subject:" str,
    # "message-id": str,
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
}

SKIPPED_HEADERS = {
    "content-transfer-encoding",
    "mime-version",
}

def email2dict(msg: Message) -> dict:
    if not isinstance(msg, EmailMessage):
        msg = message2email(msg)
    data = {"headers": {}}
    for header in msg:
        header = header.lower()
        if header in SKIPPED_HEADERS:
            continue
        values = msg.get_all(header)
        if not values:
            continue
        elif header in HEADER_PROCESSORS:
            v = HEADER_PROCESSORS[header](values)
        else:
            v = unlist(list(map(str, values)))
        data["headers"][header] = v
    data["preamble"] = msg.preamble
    if msg.is_multipart():
        data["content"] = list(map(email2dict, msg.iter_parts()))
    else:
        data["content"] = msg.get_content()
    data["epilogue"] = msg.epilogue
    return data

def message2email(msg: Message) -> EmailMessage:
    return email.message_from_bytes(bytes(msg), policy=policy.default)

def unlist(x):
    return x[0] if len(x) == 1 else x
