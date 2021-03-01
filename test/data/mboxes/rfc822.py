from copy import deepcopy
from datetime import datetime, timezone

data = {
    "unixfrom": "From sender@example.nil Sat Aug 18 03:12:23 2018",
    "headers": {
        "delivered-to": [
            "recipient@redacted.nil",
        ],
        "date": datetime(2018, 8, 18, 3, 11, 52, tzinfo=timezone.utc),
        "from": [
            {
                "display_name": "Steven E'Nder",
                "address": "sender@example.nil",
            },
        ],
        "to": [
            {
                "display_name": "",
                "address": "recipient@redacted.nil",
            },
        ],
        "subject": "Fwd: Your confirmed booking",
        "message-id": "<20180818031152.GA7082@example.nil>",
        "content-type": {
            "content_type": "multipart/mixed",
            "params": {},
        },
        "content-disposition": {
            "disposition": "inline",
            "params": {},
        },
        "user-agent": [
            "Mutt/1.5.24 (2015-08-30)",
        ],
    },
    "preamble": "",
    "content": [
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "text/plain",
                    "params": {},
                },
                "content-disposition": {
                    "disposition": "inline",
                    "params": {},
                },
            },
            "preamble": None,
            "content": "Here's that e-mail you wanted:\n\n",
            "epilogue": None,
        },
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "message/rfc822",
                    "params": {},
                },
                "content-disposition": {
                    "disposition": "inline",
                    "params": {},
                },
            },
            "preamble": None,
            "content": {
                "unixfrom": None,
                "headers": {
                    "delivered-to": [
                        "sender@example.nil",
                    ],
                    "date": datetime(2018, 8, 18, 3, 8, 20, tzinfo=timezone.utc),
                    "sender": {
                        "display_name": "",
                        "address": "hi.booker.com@company.out.foobar.qq",
                    },
                    "message-id": "<abcdefghijklmnopqrstuv@smtpd.sendgrid.net>",
                    "to": [
                        {
                            "display_name": "",
                            "address": "sender@example.nil",
                        },
                    ],
                    "from": [
                        {
                            "display_name": "Booking Company",
                            "address": "hi.booker.com@company.out.foobar.qq",
                        },
                    ],
                    "subject": "Your confirmed booking",
                    "content-type": {
                        "content_type": "text/plain",
                        "params": {},
                    },
                },
                "preamble": None,
                "content": "We have great news! Your booking has been finalized and confirmed. Enjoy your trip, and please let us know if we can be helpful in any way. \nConfirmation ABC123 \nFlight from Newark to San Francisco EWR → SFO \nAirline PanAm \nFlight Number(s) PA 1234 \nDeparture August 19, 2018 at 3:50 PM \nArrival August 19, 2018 at 7:10 PM \nLayovers Nonstop \nClass of Service Economy \nFlight from San Francisco to Newark SFO → EWR \nAirline PanAm \nFlight Number(s) PA 4321 \nDeparture August 20, 2018 at 9:30 PM \nArrival August 21, 2018 at 6:00 AM \nLayovers Nonstop \nClass of Service Economy \nTravelers Steven E'Nder \n\nThis email is a booking confirmation, not a receipt. If you used your own payment method for this purchase, you will receive a separate email receipt after you are charged. \n",
                "epilogue": None,
            },
            "epilogue": None,
        },
    ],
    "epilogue": "",
}

data_all = deepcopy(data)
data_all["headers"]["mime-version"] = "1.0"
data_all["headers"]["content-type"]["params"]["boundary"] = "cWoXeonUoKmBZSoM"
data_all["content"][0]["headers"]["content-type"]["params"]["charset"] = "us-ascii"
data_all["content"][1]["content"]["headers"]["mime-version"] = "1.0"
data_all["content"][1]["content"]["headers"]["content-type"]["params"]["charset"] = "utf-8"
data_all["content"][1]["content"]["headers"]["content-transfer-encoding"] = "quoted-printable"
