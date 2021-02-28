from copy import deepcopy

data = {
    "unixfrom": None,
    "headers": {
        "content-type": {
            "content_type": "multipart/related",
            "params": {
                "start": "<950120.aaCC@XIson.com>",
                "type": "Application/X-FixedRecord",
                "start-info": "-o ps",
            },
        },
        "comment": [
            "Taken from (errata'ed) RFC 2387, section 5.1",
        ],
    },
    "preamble": None,
    "content": [
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "application/x-fixedrecord",
                    "params": {},
                },
                "content-id": [
                    "<950120.aaCC@XIson.com>",
                ],
            },
            "preamble": None,
            "content": b"25\n10\n34\n10\n25\n21\n26\n10",
            "epilogue": None,
        },
        {
            "unixfrom": None,
            "headers": {
                "content-type": {
                    "content_type": "application/octet-stream",
                    "params": {},
                },
                "content-description": [
                    "The fixed length records",
                ],
                "content-id": [
                    "<950120.aaCB@XIson.com>",
                ],
            },
            "preamble": None,
            "content": b"Old MacDonald had a farm\nE I E I O\nAnd on his farm he had some ducks\nE I E I O\nWith a quack quack here,\na quack quack there,\nevery where a quack quack\nE I E I O\n",
            "epilogue": None,
        },
    ],
    "epilogue": "",
}

data_all = deepcopy(data)
data_all["headers"]["content-type"]["params"]["boundary"] = "example-1"
data_all["content"][1]["headers"]["content-transfer-encoding"] = "base64"
