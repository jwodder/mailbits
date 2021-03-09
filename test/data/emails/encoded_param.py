from copy import deepcopy

data = {
    "unixfrom": None,
    "headers": {
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
        "subject": "Seeking a job",
        "content-type": {
            "content_type": "multipart/mixed",
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
            "content": "Please find my credentials attached.\n\n",
            "epilogue": None,
        },
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "text/plain",
                    "params": {"name": "résumé.txt"},
                },
                "content-disposition": {
                    "disposition": "attachment",
                    "params": {"filename": "résumé.txt"},
                },
            },
            "preamble": None,
            "content": "- Wrote email2dict\n- Has a pulse (sometimes)\n",
            "epilogue": None,
        },
    ],
    "epilogue": "\n",
}

data_all = deepcopy(data)
data_all["headers"]["mime-version"] = "1.0"
data_all["headers"]["content-type"]["params"]["boundary"] = "cWoXeonUoKmBZSoM"
data_all["content"][0]["headers"]["content-type"]["params"]["charset"] = "us-ascii"
data_all["content"][1]["headers"]["content-type"]["params"]["charset"] = "us-ascii"
