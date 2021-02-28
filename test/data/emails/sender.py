from datetime import datetime, timedelta, timezone

data = {
    "headers": {
        "from": [
            {
                "realname": "John Doe",
                "address": "jdoe@machine.example",
            },
        ],
        "sender": {
            "realname": "Michael Jones",
            "address": "mjones@machine.example",
        },
        "to": [
            {
                "realname": "Mary Smith",
                "address": "mary@example.net",
            },
        ],
        "subject": "Saying Hello",
        "date": datetime(1997, 11, 21, 9, 55, 6, tzinfo=timezone(timedelta(hours=-6))),
        "message-id": "<1234@local.machine.example>",
    },
    "preamble": None,
    "content": "This is a message just to say hello.\nSo, \"Hello\".\n\n-- \nTaken from RFC 5322, section A.1.1.\n",
    "epilogue": None,
}
