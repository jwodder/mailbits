from copy import deepcopy
import email
from email import policy
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from importlib import import_module
import mailbox
from operator import attrgetter
from pathlib import Path
import pytest
from email2dict import email2dict

DATA_DIR = Path(__file__).with_name("data")
EMAIL_DIR = DATA_DIR / "emails"
MBOX_DIR = DATA_DIR / "mboxes"

def test_simple():
    BODY = (
        "Oh my beloved!\n"
        "\n"
        "Wilt thou dine with me on the morrow?\n"
        "\n"
        "We're having hot pockets.\n"
        "\n"
        "Love, Me\n"
    )
    msg = EmailMessage()
    msg["Subject"] = "Meet me"
    msg["To"] = "my.beloved@love.love"
    msg["From"] = "me@here.qq"
    msg.set_content(BODY)
    DICT = {
        "unixfrom": None,
        "headers": {
            "subject": "Meet me",
            "to": [
                {
                    "display_name": "",
                    "address": "my.beloved@love.love",
                },
            ],
            "from": [
                {
                    "display_name": "",
                    "address": "me@here.qq",
                },
            ],
            "content-type": {
                "content_type": "text/plain",
                "params": {},
            },
        },
        "preamble": None,
        "content": BODY,
        "epilogue": None,
    }
    assert email2dict(msg) == DICT
    DICT_ALL = deepcopy(DICT)
    DICT_ALL["headers"]["content-type"]["params"]["charset"] = "utf-8"
    DICT_ALL["headers"]["content-transfer-encoding"] = "7bit"
    DICT_ALL["headers"]["mime-version"] = "1.0"
    assert email2dict(msg, include_all=True) == DICT_ALL

def test_text_html_attachment():
    # Adapted from <https://docs.python.org/3/library/email.examples.html>
    msg = EmailMessage()
    msg["Subject"] = "Ayons asperges pour le déjeuner"
    msg["From"] = Address("Pepé Le Pew", "pepe", "example.com")
    msg["To"] = (Address("Penelope Pussycat", "penelope", "example.com"),
                 Address("Fabrette Pussycat", "fabrette", "example.com"))
    TEXT = (
        "Salut!\n"
        "\n"
        "Cela ressemble à un excellent recipie[1] déjeuner.\n"
        "\n"
        "[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718\n"
        "\n"
        "--Pepé\n"
    )
    msg.set_content(TEXT)
    asparagus_cid = make_msgid()
    HTML = (
        "<html>\n"
        "  <head></head>\n"
        "  <body>\n"
        "    <p>Salut!</p>\n"
        "    <p>Cela ressemble à un excellent\n"
        "        <a href=\"http://www.yummly.com/recipe/Roasted-Asparagus-"
        "Epicurious-203718\">\n"
        "            recipie\n"
        "        </a> déjeuner.\n"
        "    </p>\n"
        f"    <img src=\"cid:{asparagus_cid[1:-1]}\" />\n"
        "  </body>\n"
        "</html>\n"
    )
    msg.add_alternative(HTML, subtype='html')
    IMG = b'\1\2\3\4\5'
    msg.get_payload()[1].add_related(IMG, 'image', 'png', cid=asparagus_cid)
    DICT = {
        "unixfrom": None,
        "headers": {
            "subject": "Ayons asperges pour le déjeuner",
            "from": [
                {
                    "display_name": "Pepé Le Pew",
                    "address": "pepe@example.com",
                },
            ],
            "to": [
                {
                    "display_name": "Penelope Pussycat",
                    "address": "penelope@example.com",
                },
                {
                    "display_name": "Fabrette Pussycat",
                    "address": "fabrette@example.com",
                },
            ],
            "content-type": {
                "content_type": "multipart/alternative",
                "params": {},
            },
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
                "content": TEXT,
                "epilogue": None,
            },
            {
                "unixfrom": None,
                "headers": {
                    "content-type": {
                        "content_type": "multipart/related",
                        "params": {},
                    },
                },
                "preamble": None,
                "content": [
                    {
                        "unixfrom": None,
                        "headers": {
                            "content-type": {
                                "content_type": "text/html",
                                "params": {},
                            },
                        },
                        "preamble": None,
                        "content": HTML,
                        "epilogue": None,
                    },
                    {
                        "unixfrom": None,
                        "headers": {
                            "content-type": {
                                "content_type": "image/png",
                                "params": {},
                            },
                            "content-disposition": {
                                "disposition": "inline",
                                "params": {},
                            },
                            "content-id": [asparagus_cid],
                        },
                        "preamble": None,
                        "content": IMG,
                        "epilogue": None,
                    },
                ],
                "epilogue": None,
            },
        ],
        "epilogue": None,
    }
    assert email2dict(msg) == DICT
    DICT_ALL = deepcopy(DICT)
    DICT_ALL["headers"]["mime-version"] = "1.0"
    DICT_ALL["content"][0]["headers"]["content-transfer-encoding"] = "8bit"
    DICT_ALL["content"][0]["headers"]["content-type"]["params"]["charset"] = "utf-8"
    DICT_ALL["content"][1]["headers"]["mime-version"] = "1.0"
    DICT_ALL["content"][1]["content"][0]["headers"]["content-transfer-encoding"] = "quoted-printable"
    DICT_ALL["content"][1]["content"][0]["headers"]["content-type"]["params"]["charset"] = "utf-8"
    DICT_ALL["content"][1]["content"][1]["headers"]["mime-version"] = "1.0"
    DICT_ALL["content"][1]["content"][1]["headers"]["content-transfer-encoding"] = "base64"
    assert email2dict(msg, include_all=True) == DICT_ALL

@pytest.mark.parametrize("eml", EMAIL_DIR.glob("*.eml"), ids=attrgetter("name"))
def test_actual_emails(eml, monkeypatch):
    with eml.open("rb") as fp:
        msg = email.message_from_binary_file(fp, policy=policy.default)
    monkeypatch.syspath_prepend(EMAIL_DIR)
    module = import_module(eml.stem)
    assert email2dict(msg) == module.data
    assert email2dict(msg, include_all=True) == module.data_all

@pytest.mark.parametrize("mbox", MBOX_DIR.glob("*.mbox"), ids=attrgetter("name"))
def test_actual_mboxes(mbox, monkeypatch):
    box = mailbox.mbox(mbox)
    box.lock()
    msg, = box
    box.close()
    monkeypatch.syspath_prepend(MBOX_DIR)
    module = import_module(mbox.stem)
    assert email2dict(msg) == module.data
    assert email2dict(msg, include_all=True) == module.data_all

def test_text_image_mixed():
    PNG = bytes.fromhex(
        '89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52'
        '00 00 00 10 00 00 00 10  08 06 00 00 00 1f f3 ff'
        '61 00 00 00 06 62 4b 47  44 00 ff 00 ff 00 ff a0'
        'bd a7 93 00 00 00 09 70  48 59 73 00 00 00 48 00'
        '00 00 48 00 46 c9 6b 3e  00 00 00 09 76 70 41 67'
        '00 00 00 10 00 00 00 10  00 5c c6 ad c3 00 00 00'
        '5b 49 44 41 54 38 cb c5  92 51 0a c0 30 08 43 7d'
        'b2 fb 5f 39 fb 12 da 61  a9 c3 8e f9 a7 98 98 48'
        '90 64 9d f2 16 da cc ae  b1 01 26 39 92 d8 11 10'
        '16 9e e0 8c 64 dc 89 b9  67 80 ca e5 f3 3f a8 5c'
        'cd 76 52 05 e1 b5 42 ea  1d f0 91 1f b4 09 78 13'
        'e5 52 0e 00 ad 42 f5 bf  85 4f 14 dc 46 b3 32 11'
        '6c b1 43 99 00 00 00 00  49 45 4e 44 ae 42 60 82'
    )
    body = EmailMessage()
    body.set_content("This is part 1.\n")
    image = EmailMessage()
    image.set_content(
        PNG,
        "image",
        "png",
        disposition = "inline",
        filename = "ternary.png",
    )
    msg = EmailMessage()
    msg["Subject"] = "Text and an image"
    msg.make_mixed()
    msg.attach(body)
    msg.attach(image)
    DICT = {
        "unixfrom": None,
        "headers": {
            "subject": "Text and an image",
            "content-type": {
                "content_type": "multipart/mixed",
                "params": {},
            },
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
                "content": "This is part 1.\n",
                "epilogue": None,
            },
            {
                "unixfrom": None,
                "headers": {
                    "content-type": {
                        "content_type": "image/png",
                        "params": {},
                    },
                    "content-disposition": {
                        "disposition": "inline",
                        "params": {
                            "filename": "ternary.png",
                        },
                    },
                },
                "preamble": None,
                "content": PNG,
                "epilogue": None,
            },
        ],
        "epilogue": None,
    }
    assert email2dict(msg) == DICT
    DICT_ALL = deepcopy(DICT)
    DICT_ALL["content"][0]["headers"]["mime-version"] = "1.0"
    DICT_ALL["content"][0]["headers"]["content-transfer-encoding"] = "7bit"
    DICT_ALL["content"][0]["headers"]["content-type"]["params"]["charset"] = "utf-8"
    DICT_ALL["content"][1]["headers"]["mime-version"] = "1.0"
    DICT_ALL["content"][1]["headers"]["content-transfer-encoding"] = "base64"
    assert email2dict(msg, include_all=True) == DICT_ALL
