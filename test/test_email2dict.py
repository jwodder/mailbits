from email.message import EmailMessage
from email2dict import email2dict

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
