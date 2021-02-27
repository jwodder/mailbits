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

def process_unique_addr_headers(uahs):
    data = []
    for h in uahs:
        for g in h.groups:
            if g.display_name is not None:
                group = {"group": g.display_name, "addresses": []}
                data.append(group)
                addrlist = group["addresses"]
            else:
                addrlist = data
            for a in g.addresses:
                addrlist.append(
                    {
                        "realname": a.display_name,
                        "address": a.addr_spec,
                    }
                )
    return data

def process_content_type_headers(cths):
    # Discard params
    return unlist([h.content_type for h in cths])


HEADER_PROCESSORS = {
    "from": process_unique_addr_headers,
    "to": process_unique_addr_headers,
    "cc": process_unique_addr_headers,
    "bcc": process_unique_addr_headers,
    "content-type": process_content_type_headers,
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
    if msg.is_multipart():
        data["content"] = list(map(email2dict, msg.iter_parts()))
    else:
        data["content"] = msg.get_content()
    return data

def message2email(msg: Message) -> EmailMessage:
    return email.message_from_bytes(bytes(msg), policy=policy.default)

def unlist(x):
    return x[0] if len(x) == 1 else x
