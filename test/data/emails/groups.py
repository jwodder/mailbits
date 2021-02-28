from datetime import datetime, timedelta, timezone

data = {
    "unixfrom": None,
    "headers": {
        "from": [
            {
                "display_name": "Pete",
                "address": "pete@silly.example",
            },
        ],
        "to": [
            {
                "group": "A Group",
                "addresses": [
                    {
                        "display_name": "Ed Jones",
                        "address": "c@a.test",
                    },
                    {
                        "display_name": "",
                        "address": "joe@where.test",
                    },
                    {
                        "display_name": "John",
                        "address": "jdoe@one.test",
                    },
                ],
            },
        ],
        "cc": [
            {
                "group": "Undisclosed recipients",
                "addresses": [],
            },
        ],
        "date": datetime(1969, 2, 13, 23, 32, 54, tzinfo=timezone(-timedelta(hours=3, minutes=30))),
        "message-id": "<testabcd.1234@silly.example>",
    },
    "preamble": None,
    "content": "Testing.\n\n-- \nTaken from RFC 5322, section A.1.3.\n",
    "epilogue": None,
}

data_all = data
