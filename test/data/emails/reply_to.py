from datetime import datetime, timedelta, timezone

data = {
    "unixfrom": None,
    "headers": {
        "from": [
            {
                "display_name": "Mary Smith",
                "address": "mary@example.net",
            },
        ],
        "to": [
            {
                "display_name": "John Doe",
                "address": "jdoe@machine.example",
            },
        ],
        "reply-to": [
            {
                "display_name": "Mary Smith: Personal Account",
                "address": "smith@home.example",
            },
        ],
        "subject": "Re: Saying Hello",
        "date": datetime(1997, 11, 21, 10, 1, 10, tzinfo=timezone(timedelta(hours=-6))),
        "message-id": "<3456@example.net>",
        "in-reply-to": [
            "<1234@local.machine.example>",
        ],
        "references": [
            "<1234@local.machine.example>",
        ],
    },
    "preamble": None,
    "content": "This is a reply to your hello.\n\n-- \nTaken from RFC 5322, section A.2.\n",
    "epilogue": None,
}

data_all = data
