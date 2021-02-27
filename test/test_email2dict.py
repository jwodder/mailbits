from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from email2dict import email2dict

DATA_DIR = Path(__file__).with_name("data")

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
    assert email2dict(msg) == {
        "headers": {
            "subject": "Meet me",
            "to": [
                {
                    "realname": "",
                    "address": "my.beloved@love.love",
                },
            ],
            "from": [
                {
                    "realname": "",
                    "address": "me@here.qq",
                },
            ],
            "content-type": "text/plain",
        },
        "content": BODY,
    }

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
    # Asparagus clipart courtesy of <https://www.clipartmax.com/middle/
    # m2i8i8G6N4i8G6G6_asparagus-clip-art-free-clip-art-asparagus/>
    with (DATA_DIR / "asparagus.png").open("rb") as fp:
        IMG = fp.read()
    msg.get_payload()[1].add_related(IMG, 'image', 'png', cid=asparagus_cid)
    assert email2dict(msg) == {
        "headers": {
            "subject": "Ayons asperges pour le déjeuner",
            "from": [
                {
                    "realname": "Pepé Le Pew",
                    "address": "pepe@example.com",
                },
            ],
            "to": [
                {
                    "realname": "Penelope Pussycat",
                    "address": "penelope@example.com",
                },
                {
                    "realname": "Fabrette Pussycat",
                    "address": "fabrette@example.com",
                },
            ],
            "content-type": "multipart/alternative",
        },
        "content": [
            {
                "headers": {
                    "content-type": "text/plain"
                },
                "content": TEXT,
            },
            {
                "headers": {
                    "content-type": "multipart/related",
                },
                "content": [
                    {
                        "headers": {
                            "content-type": "text/html",
                        },
                        "content": HTML,
                    },
                    {
                        "headers": {
                            "content-type": "image/png",
                            "content-disposition": "inline",
                            "content-id": asparagus_cid,
                        },
                        "content": IMG,
                    },
                ],
            },
        ]
    }
