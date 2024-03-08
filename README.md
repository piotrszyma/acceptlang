# Simple package for parsing Accept-Language tag.

This package can be used in the server environment to parse the Accept-Language
header.

Test cases and code copied from Django source code enhanced with typing.

Purpose of this code is to be able to use a battle-tested Accept-Language
parsing logic in Python code without need to install Django package.

# Local development

```sh
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.dev.txt
```
