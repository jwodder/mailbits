v0.2.2 (2024-12-01)
-------------------
- Support Python 3.10, 3.11, 3.12, and 3.13
- Drop support for Python 3.6 and 3.7
- Migrated from setuptools to hatch

v0.2.1 (2021-03-16)
-------------------
- Change type of `ContentType.params` to `Dict[str, str]`

v0.2.0 (2021-03-13)
-------------------
- Renamed project from "email2dict" to "mailbits"
- Added a `ContentType` class
- Exposed the `message2email()` function
- Exposed the `MessageDict` type
- Added the following functions:
    - `format_addresses()`
    - `parse_address()`
    - `parse_addresses()`
    - `recipient_addresses()`

v0.1.0 (2021-02-28)
-------------------
Initial release
