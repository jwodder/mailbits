from copy import deepcopy
from datetime import datetime, timezone

data = {
    "unixfrom": "From 0101017629c51320-4f67ae0a-8056-4cd7-b526-e47da4bbe7b7-000000@ses.pypi.org  Thu Dec  3 18:07:47 2020",
    "headers": {
        "return-path": [
            "<0101017629c51320-4f67ae0a-8056-4cd7-b526-e47da4bbe7b7-000000@ses.pypi.org>",
        ],
        "x-original-to": [
            "recipient@redacted.nil",
        ],
        "delivered-to": [
            "recipient@redacted.nil",
        ],
        "x-greylist": [
            "delayed 316 seconds by postgrey-1.36 at firefly; Thu, 03 Dec 2020 18:07:47 UTC",
        ],
        "authentication-results": [
            "mail.redacted.nil;\tdkim=pass (1024-bit key; unprotected) header.d=pypi.org header.i=@pypi.org header.a=rsa-sha256 header.s=sy4yaueax2wxeqvbwtfafsfpuli4zspd header.b=RopfsgK8;\tdkim=pass (1024-bit key; unprotected) header.d=amazonses.com header.i=@amazonses.com header.a=rsa-sha256 header.s=hsbnp7p3ensaochzwyq5wwmceodymuwv header.b=PvoEs17L;\tdkim-atps=neutral",
        ],
        "received": [
            "from a27-10.smtp-out.us-west-2.amazonses.com (a27-10.smtp-out.us-west-2.amazonses.com [54.240.27.10])\tby mail.redacted.nil (Postfix) with ESMTPS id 5EAAE13B030\tfor <recipient@redacted.nil>; Thu,  3 Dec 2020 18:07:47 +0000 (UTC)",
        ],
        "dkim-signature": [
            "v=1; a=rsa-sha256; q=dns/txt; c=relaxed/simple;\ts=sy4yaueax2wxeqvbwtfafsfpuli4zspd; d=pypi.org; t=1607018550;\th=Subject:From:To:MIME-Version:Content-Type:Message-ID:Date;\tbh=3tSjr/p8U98Y6VPb/lXnFWQX4OvAj20xcNdTK2v2o6k=;\tb=RopfsgK8yiLka57yfeNmWJKg4i6ToHif2+7H8gRketwz+0QfsjU/mRcGJUkVOGVQ\tv2wlDwboRC2G39QbX53YYyo4yQBPXokRImT8xRkDpHomqd0OUS0odtE8THHack8EEaE\t3gfX+t80fHbILQiNtAyjXg60IlivJemzFEs93tks=",
            "v=1; a=rsa-sha256; q=dns/txt; c=relaxed/simple;\ts=hsbnp7p3ensaochzwyq5wwmceodymuwv; d=amazonses.com; t=1607018550;\th=Subject:From:To:MIME-Version:Content-Type:Message-ID:Date:Feedback-ID;\tbh=3tSjr/p8U98Y6VPb/lXnFWQX4OvAj20xcNdTK2v2o6k=;\tb=PvoEs17LVcXnf9YScJ9IPD4pVhs1mzl4YYGv2fCT0oG7xdKodFSlZJ7Z0haY1APE\tT86HnVq7bzjsCWL9TQJWAi+LrHBlIRLRL22k6YNDuwYJOa9dkKFxbiaqwEIe+bzxuEX\tPpdWM/1xxHuQ9a11INQRSH8it0sZXwSTBTqRyaAU=",
        ],
        "subject": "[PyPI] Collaborator added notification",
        "from": [
            {
                "display_name": "PyPI",
                "address": "noreply@pypi.org",
            },
        ],
        "to": [
            {
                "display_name": "jwodder",
                "address": "recipient@redacted.nil",
            },
        ],
        "content-type": {
            "content_type": "multipart/alternative",
            "params": {},
        },
        "message-id": "<0101017629c51320-4f67ae0a-8056-4cd7-b526-e47da4bbe7b7-000000@us-west-2.amazonses.com>",
        "date": datetime(2020, 12, 3, 18, 2, 30, tzinfo=timezone.utc),
        "x-ses-outgoing": [
            "2020.12.03-54.240.27.10",
        ],
        "feedback-id": [
            "1.us-west-2.ZRFc7KXPaRh5E01FOWpg1s1VfcS7E0CO2O03ZZnJB3U=:AmazonSES",
        ],
        "status": ["RO"],
        "content-length": ["1431"],
        "lines": ["65"],
    },
    "preamble": None,
    "content": [
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "text/plain",
                    "params": {},
                },
            },
            "preamble": None,
            "content": "\nA new collaborator has been added to a project you own on PyPI:\n\n  Username: REDACTED\n  Role: Owner\n  Collaborator for: REDACTED\n  Added by: jwodder\n\nIf this was a mistake, you can email admin@pypi.org to communicate with the PyPI administrators.\n\n\n--\n\nYou are receiving this because you are an owner of this project.\n",
            "epilogue": None,
        },
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "text/html",
                    "params": {},
                },
            },
            "preamble": None,
            "content": "<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width\">\n\n    </head>\n  <body>\n    \n<p>\n  A new collaborator has been added to a project you own on PyPI:\n\n  </p>\n<ul style=\"list-style-type:none\">\n    <li>\n<strong>Username</strong>: REDACTED</li>\n    <li>\n<strong>Role</strong>: Owner</li>\n    <li>\n<strong>Collaborator for</strong>: REDACTED</li>\n    <li>\n<strong>Added by</strong>: jwodder</li>\n  </ul>\n\n\n<p>If this was a mistake, you can email <a href=\"mailto:admin@pypi.org\">admin@pypi.org</a> to communicate with the PyPI administrators.</p>\n\n\n    \n    <p style=\"color:#666; font-size:small\">\n        —<br>\n        \nYou are receiving this because you are an owner of this project.\n\n    </p>\n    \n  </body>\n</html>\n",
            "epilogue": None,
        },
    ],
    "epilogue": "",
}

data_all = deepcopy(data)
data_all["headers"]["mime-version"] = "1.0"
data_all["headers"]["content-type"]["params"]["boundary"] = "===============0747615486913937503=="
data_all["content"][0]["headers"]["content-type"]["params"]["charset"] = "utf-8"
data_all["content"][0]["headers"]["content-transfer-encoding"] = "7bit"
data_all["content"][1]["headers"]["content-type"]["params"]["charset"] = "utf-8"
data_all["content"][1]["headers"]["content-transfer-encoding"] = "quoted-printable"
data_all["content"][1]["headers"]["mime-version"] = "1.0"
