from datetime import datetime, timedelta, timezone

data = {
    "unixfrom": None,
    "headers": {
        "resent-from": [
            {
                "display_name": "Mary Smith",
                "address": "mary@example.net",
            },
        ],
        "resent-sender": [
            {
                "display_name": "Michael Jones",
                "address": "mjones@machine.example",
            },
        ],
        "resent-to": [
            {
                "display_name": "Jane Brown",
                "address": "j-brown@other.example",
            },
        ],
        "resent-date": [
            datetime(1997, 11, 24, 14, 22, 1, tzinfo=timezone(timedelta(hours=-8))),
        ],
        "resent-message-id": [
            "<78910@example.net>",
        ],
        "from": [
            {
                "display_name": "John Doe",
                "address": "jdoe@machine.example",
            },
        ],
        "to": [
            {
                "display_name": "Mary Smith",
                "address": "mary@example.net",
            },
        ],
        "subject": "Saying Hello",
        "date": datetime(1997, 11, 21, 9, 55, 6, tzinfo=timezone(timedelta(hours=-6))),
        "message-id": "<1234@local.machine.example>",
    },
    "preamble": None,
    "content": "This is a message just to say hello.\nSo, \"Hello\".\n\n-- \nAdapted from RFC 5322, section A.3.\n",
    "epilogue": None,
}

data_all = data
