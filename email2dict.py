import email
from email import policy
from email.message import EmailMessage, Message
from typing import Any

def process_unique_addr_header(uah):
    data = []
    for g in uah.groups:
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


HEADER_PROCESSORS = {
    "subject": str,
    "from": process_unique_addr_header,
    "to": process_unique_addr_header,
    "cc": process_unique_addr_header,
    "bcc": process_unique_addr_header,
}

def email2dict(msg: Message) -> dict:
    if not isinstance(msg, EmailMessage):
        msg = message2email(msg)
    data = {"headers": {}}
    for header in msg:
        header = header.lower()
        value: Any
        value = msg.get_all(header)
        assert isinstance(value, list)
        if len(value) == 1:
            value = value[0]
        elif not value:
            continue
        data["headers"][header] = value
    data["content-type"] = msg.get_content_type()
    if msg.is_multipart():
        data["content"] = list(map(email2dict, msg.iter_parts()))
    else:
        data["content"] = msg.get_content()
    return data

def message2email(msg: Message) -> EmailMessage:
    return email.message_from_bytes(bytes(msg), policy=policy.default)
