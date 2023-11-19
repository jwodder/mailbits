v0.3.0 (in development)
-----------------------
- Support Python 3.10, 3.11, and 3.12
- Drop support for Python 3.6
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
