# Simple package for parsing Accept-Language tag.

This package can be used in the server environment to parse the Accept-Language
header.

Test cases and code copied from Django source code enhanced with typing.

Purpose of this code is to be able to use a battle-tested Accept-Language
parsing logic in Python code without need to install Django package.

## Installation

You can install the package via pip:

```sh
pip install acceptlang
```

## Usage

```python
from acceptlang import parse_accept_lang_header

result = parse_accept_lang_header("en-us,en;q=0.5,de;q=0.3")
assert result == (('en-us', 1.0), ('en',0.5), ('de',0.3))

result = parse_accept_lang_header("en-us,*;q=0.5")
assert result == (('en-us', 1.0), ('*',0.5))
```

Check [tests](tests/test_parse.py) for more examples.

# Local development

```sh
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.dev.txt
```

# Build and publish

```sh
python3 -m build --wheel
twine check dist/**
twine upload dist/
```
