from copy import deepcopy
from datetime import datetime, timedelta, timezone

data = {
    "unixfrom": None,
    "headers": {
        "delivered-to": ["recipient@redacted.nil"],
        "received": [
            "by 2002:ac0:a2c2:0:0:0:0:0 with SMTP id 60csp4719765imt;        Mon, 28 Dec 2020 07:07:19 -0800 (PST)",
            "from mail.python.org (mail.python.org. [188.166.95.178])        by mx.google.com with ESMTPS id by27si18939218edb.276.2020.12.28.07.07.19        for <recipient@redacted.nil>        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 bits=256/256);        Mon, 28 Dec 2020 07:07:19 -0800 (PST)",
            "from mail.python.org (mail1.ams1.psf.io [127.0.0.1])\tby mail.python.org (Postfix) with ESMTP id 4D4LWC07XmzpFYf\tfor <recipient@redacted.nil>; Mon, 28 Dec 2020 10:07:19 -0500 (EST)",
            "from mail.python.org (mail1.ams1.psf.io [127.0.0.1])\tby mail.python.org (Postfix) with ESMTP id 4D1nTl11NLzpFQk\tfor <distutils-sig@python.org>; Thu, 24 Dec 2020 06:12:11 -0500 (EST)",
            "from mail1.ams1.psf.io (HELO mail.python.org) (127.0.0.1)  by mail.python.org with SMTP; 24 Dec 2020 06:12:11 -0500",
            "from mail-ej1-x62d.google.com (mail-ej1-x62d.google.com [IPv6:2a00:1450:4864:20::62d])\t(using TLSv1.3 with cipher TLS_AES_256_GCM_SHA384 (256/256 bits)\t key-exchange X25519 server-signature RSA-PSS (2048 bits) server-digest SHA256)\t(No client certificate requested)\tby mail.python.org (Postfix) with ESMTPS\tfor <distutils-sig@python.org>; Thu, 24 Dec 2020 06:12:10 -0500 (EST)",
            "by mail-ej1-x62d.google.com with SMTP id w1so2888903ejf.11        for <distutils-sig@python.org>; Thu, 24 Dec 2020 03:12:10 -0800 (PST)",
        ],
        "x-google-smtp-source": [
            "ABdhPJzA/Taij6vwL6SyA+Fl8im5Y84Os0+Hk7RimG4HmDdtm6X5GLYDTv2QQr/H9u50/8w93C4/",
        ],
        "x-received": [
            "by 2002:a17:906:878d:: with SMTP id za13mr41554256ejb.395.1609168039403;        Mon, 28 Dec 2020 07:07:19 -0800 (PST)",
            "by 2002:a17:907:2108:: with SMTP id qn8mr27369460ejb.127.1608808330208; Thu, 24 Dec 2020 03:12:10 -0800 (PST)",
        ],
        "arc-seal": [
            "i=1; a=rsa-sha256; t=1609168039; cv=none;        d=google.com; s=arc-20160816;        b=umN621V3wTbn5iGxVRov5MOa9vXGY3b/KQgYrJEIVWs3vRpkw/iWuQcsbcG6h6iHWz         ch3yAHtHhvYktFV1iR5e+NlEueY6V5QT4yW1impStJWqW4CN3bEOgvHAXJ2KwNOSrr3K         cFW+1R39QqYn1P9zv5HpLvP2isI1/WZQXxc7UsJ1JaMN2146ioFKtzVb06n9AGAmHAtj         OTpUQQnF1AemCmT0Ge2Q//bhErXn6xUcuwEN5enAW9NYPCgyGw7UZ4YADUjBJ3fopNUX         hi7KnWVMiZP2XwOVbsIIbE9TahhmCa4WRkPA2vY+Ne8UbKzpO4Y2xMIMxv2Mc2IUUc9q         WsSQ==",
        ],
        "arc-message-signature": [
            "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=list-unsubscribe:list-subscribe:list-post:list-help:list-archive         :archived-at:list-id:subject:precedence:message-id-hash:to         :message-id:date:from:mime-version:dkim-signature:dkim-signature;        bh=HqMw7IM1Rimz/7z4Mk+sE6QIRK23hm2DEzjUCvPEmAI=;        b=vd7Sx2kOx6PZKpQB/eouARKfHSYwGH5Pj241HhAmdSMMDS3CGkjir+lvuhtQ3kjo7b         FNROpjqtAzl4eJ3F3EMYo+j8Tt/NLHLnwiwpbqJVdHO+suVbKrQ9oidOPj6QWrgavk7n         V9De8kMDlBlpiUhp8K0IWA4VBa3qcfKIZHqukQovqqyx1LOqTg2NwcHemma7d2ky/Ue/         lClTsGlBD7O4gsoFtyDRzdvmCya/VB9l8J6A3qAwHCbabzRFN8hBHdYjD1EjUo+d2fCy         LHhZIw6iPILaUS+q6V1vFC6Y1dHbErpUpNQygCp61DQTs4KBxnZGam6u/MtUW2gvA6Jv         /q0A==",
        ],
        "arc-authentication-results": [
            "i=1; mx.google.com;       dkim=pass header.i=@python.org header.s=200901 header.b=aBfU1fxY;       dkim=neutral (body hash did not verify) header.i=@gmail.com header.s=20161025 header.b=amXVzdXG;       spf=pass (google.com: domain of distutils-sig-bounces+recipient=redacted.nil@python.org designates 188.166.95.178 as permitted sender) smtp.mailfrom=\"distutils-sig-bounces+recipient=redacted.nil@python.org\";       dmarc=fail (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
        ],
        "return-path": [
            "<distutils-sig-bounces+recipient=redacted.nil@python.org>",
        ],
        "received-spf": [
            "pass (google.com: domain of distutils-sig-bounces+recipient=redacted.nil@python.org designates 188.166.95.178 as permitted sender) client-ip=188.166.95.178;",
        ],
        "authentication-results": [
            "mx.google.com;       dkim=pass header.i=@python.org header.s=200901 header.b=aBfU1fxY;       dkim=neutral (body hash did not verify) header.i=@gmail.com header.s=20161025 header.b=amXVzdXG;       spf=pass (google.com: domain of distutils-sig-bounces+recipient=redacted.nil@python.org designates 188.166.95.178 as permitted sender) smtp.mailfrom=\"distutils-sig-bounces+recipient=redacted.nil@python.org\";       dmarc=fail (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
            "mail.python.org; dkim=pass\treason=\"2048-bit key; unprotected key\"\theader.d=gmail.com header.i=@gmail.com header.b=amXVzdXG;\tdkim-adsp=pass; dkim-atps=neutral",
        ],
        "dkim-signature": [
            "v=1; a=rsa-sha256; c=relaxed/simple; d=python.org; s=200901;\tt=1609168039; bh=HqMw7IM1Rimz/7z4Mk+sE6QIRK23hm2DEzjUCvPEmAI=;\th=From:Date:To:Subject:List-Id:List-Archive:List-Help:List-Post:\t List-Subscribe:List-Unsubscribe:From;\tb=aBfU1fxYMEarNvHY5G2dwqBwz+oYnqa2Qzpn1oYoPF8b0ANMQ6uXThvuHC5hAMQvo\t hkpxvtNSmUloOrHR1xNIUc8LNnteN6n8Gp+9fRhNAFL9I5JCeensUHnK7yhb6K4Qo1\t 0uH2RI2zNtgkMzfhj5dd22mKaCeURTVuQ268S7OA=",
            "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20161025;        h=mime-version:from:date:message-id:subject:to;        bh=gA+0zvQbFGXK6SfGpDQYT7ZyNP+hEupURUMiqONEWZE=;        b=amXVzdXG3Fs3j2JL1GN6HZe3tFlHNSCiSN1oY5+ohCVbVkHTn7+ZyJ+jSUw/Hpwc7U         SvAmNjJ+nALjUxL7rOvZH3D4VpwuA9ngdW0evz2WdKXUxPd9/61iGMQfxrYVxp/huLmw         BfNqe7YvT+x5INw+capdy0EzTfJj/EfG4SQ2a0Tz7TxwDIr8YkQgUBIIxNZ//xVSzoD1         gtZRua7iEso6iLcV/r2CMYj3rNaMTFPLg4zlJt/u7PYmBOdBuK/4pwSsI8w8eI9bqms2         cfLPVV/RNeIzGVcKOlxJCOK+ctRCD/6E9ZXtSZFzq7WnKnKDBgpHBC40xGKLyPs3VHkX         vVHw==",
        ],
        "x-spam-status": [
            "OK 0.007",
        ],
        "x-spam-evidence": [
            "'*H*': 0.99; '*S*': 0.00; 'url-ip:151.101.0.223/32':    0.09; 'url-ip:151.101.128.223/32': 0.09; 'url-    ip:151.101.192.223/32': 0.09; 'url-ip:151.101.64.223/32': 0.09;    'notable': 0.16; 'upload': 0.16; 'url:latest': 0.16;    'url:project': 0.16; 'url:pypi': 0.16; 'option': 0.23; 'message-    id:@mail.gmail.com': 0.33; 'improvements': 0.33;    'received:google.com': 0.34; 'from:addr:gmail.com': 0.35;    'include': 0.38; 'to:addr:distutils-sig': 0.68",
        ],
        "x-google-dkim-signature": [
            "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20161025;        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;        bh=gA+0zvQbFGXK6SfGpDQYT7ZyNP+hEupURUMiqONEWZE=;        b=Y/6X+bpP7SHCvrsZRpV6yeQ6l5FQPmnTuagQwZaVoCshovoOi0+FHDfRgp+dkaWV+K         JMRyLWJXEKOnjM1sawBnG2LxRFeVwqhxrajrXIHfctQzBs0Qe62Hd6ZTLLFKrYvKz5Rh         5nZgeRf2i0NqlJGcDlFUGB9Bs+7KF8+d6M7QFvj08H9M7roIBQWqdvMbUA0m8BUzzNVO         qvVIDB6nsWuhBWlR2X24e1CUrzb5E++X/2BuVWasL0ZoaAzqhKN+ikycPMeCLmCQ8kxg         J+Q+0ntj1aN5yeZ+1N4/uNz52Om2bh0RU/aJ7zYcfjYLMmXhZ7Jasb8+ramfsb34Vfwm         3ZOw==",
        ],
        "x-gm-message-state": [
            "AOAM531pZltQDlpsqrcuHPwXpusl/KUwJQiaT1WBiG3Q0iVXWBBPa62s\tSZ3xcR6VvMO9Z1Ezdn5ufVoKkFmVjfR1MNRr3iDpDl7t0nwpqg=="
        ],
        "from": [
            {
                "display_name": "Brian Rutledge",
                "address": "bhrutledge@gmail.com",
            }
        ],
        "date": datetime(2020, 12, 24, 6, 11, 59, tzinfo=timezone(timedelta(hours=-5))),
        "message-id": "<CAKQj8i4mZQGGtmLe+rHAZNBXNv2Hw6dg5cHtzQL6e71mnZkanA@mail.gmail.com>",
        "to": [
            {
                "display_name": "",
                "address": "distutils-sig@python.org",
            },
        ],
        "x-mailfrom": ["bhrutledge@gmail.com"],
        "x-mailman-rule-hits": ["member-moderation"],
        "x-mailman-rule-misses": ["dmarc-mitigation; no-senders; approved; emergency; loop; banned-address"],
        "message-id-hash": ["5FC6OKCCVOJZGRYTKAK7CA5RC2XVX24Z"],
        "x-message-id-hash": ["5FC6OKCCVOJZGRYTKAK7CA5RC2XVX24Z"],
        "x-mailman-approved-at": ["Mon, 28 Dec 2020 10:06:20 -0500"],
        "x-mailman-version": ["3.3.3b1"],
        "precedence": ["list"],
        "subject": "[Distutils] Twine 3.3.0 released",
        "list-id": ["\"Python packaging ecosystem SIG (PyPI/pip/twine/wheel/setuptools/distutils/etc)\" <distutils-sig.python.org>"],
        "archived-at": ["<https://mail.python.org/archives/list/distutils-sig@python.org/message/5FC6OKCCVOJZGRYTKAK7CA5RC2XVX24Z/>"],
        "list-archive": ["<https://mail.python.org/archives/list/distutils-sig@python.org/>"],
        "list-help": ["<mailto:distutils-sig-request@python.org?subject=help>"],
        "list-post": ["<mailto:distutils-sig@python.org>"],
        "list-subscribe": ["<mailto:distutils-sig-join@python.org>"],
        "list-unsubscribe": ["<mailto:distutils-sig-leave@python.org>"],
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
                    "content": "https://pypi.org/project/twine/3.3.0/\n\nChangelog (now via towncrier):\nhttps://twine.readthedocs.io/en/latest/changelog.html\n\nNotable improvements include more `twine upload --verbose` output, and a\n`--strict` option for `twine check`.\n",
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
                    "content": "<div dir=\"ltr\"><div><a href=\"https://pypi.org/project/twine/3.3.0/\">https://pypi.org/project/twine/3.3.0/</a></div><div><br></div><div>Changelog (now via towncrier): <a href=\"https://twine.readthedocs.io/en/latest/changelog.html\">https://twine.readthedocs.io/en/latest/changelog.html</a></div><div><br></div><div>Notable improvements include more `twine upload --verbose` output, and a `--strict` option for `twine check`.</div></div>\n",
                    "epilogue": None,
                },
            ],
            "epilogue": "",
        },
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
            "content": "--\nDistutils-SIG mailing list -- distutils-sig@python.org\nTo unsubscribe send an email to distutils-sig-leave@python.org\nhttps://mail.python.org/mailman3/lists/distutils-sig.python.org/\nMessage archived at https://mail.python.org/archives/list/distutils-sig@python.org/message/5FC6OKCCVOJZGRYTKAK7CA5RC2XVX24Z/\n",
            "epilogue": None,
        },
    ],
    "epilogue": "",
}

data_all = deepcopy(data)
data_all["headers"]["mime-version"] = "1.0"
data_all["headers"]["content-type"]["params"]["boundary"] = "===============5457169869532207506=="
data_all["content"][0]["headers"]["content-type"]["params"]["boundary"] = "00000000000008a9d405b733e1f4"
data_all["content"][0]["content"][0]["headers"]["content-type"]["params"]["charset"] = "UTF-8"
data_all["content"][0]["content"][1]["headers"]["content-type"]["params"]["charset"] = "UTF-8"
data_all["content"][0]["content"][1]["headers"]["content-transfer-encoding"] = "quoted-printable"
data_all["content"][1]["headers"]["content-type"]["params"]["charset"] = "us-ascii"
data_all["content"][1]["headers"]["mime-version"] = "1.0"
data_all["content"][1]["headers"]["content-transfer-encoding"] = "7bit"
