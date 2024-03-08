# Maximum number of characters that will be parsed from the Accept-Language
# header to prevent possible denial of service or memory exhaustion attacks.
# About 10x longer than the longest value shown on MDN’s Accept-Language page.
import functools
import re
from typing import NamedTuple


class LangTag(NamedTuple):
    name: str
    priority: float


# Maximum number of characters that will be parsed from the Accept-Language
# header to prevent possible denial of service or memory exhaustion attacks.
# About 10x longer than the longest value shown on MDN’s Accept-Language page.
_ACCEPT_LANGUAGE_HEADER_MAX_LENGTH = 500

# Format of Accept-Language header values. From RFC 9110 Sections 12.4.2 and
# 12.5.4, and RFC 5646 Section 2.1.
_accept_language_re = re.compile(
    r"""
        # "en", "en-au", "x-y-z", "es-419", "*"
        ([A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*|\*)
        # Optional "q=1.00", "q=0.8"
        (?:\s*;\s*q=(0(?:\.[0-9]{,3})?|1(?:\.0{,3})?))?
        # Multiple accepts per header.
        (?:\s*,\s*|$)
    """,
    re.VERBOSE,
)


@functools.lru_cache(maxsize=1000)
def _parse_accept_lang_header(lang_string: str) -> tuple[LangTag, ...]:
    """
    Parse the lang_string, which is the body of an HTTP Accept-Language
    header, and return a tuple of (lang, q-value), ordered by 'q' values.

    Return an empty tuple if there are any format errors in lang_string.
    """
    result: list[LangTag] = []
    pieces = _accept_language_re.split(lang_string.lower())
    if pieces[-1]:
        return tuple[LangTag]()
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i : i + 3]
        if first:
            return tuple[LangTag]()
        if priority:
            priority = float(priority)
        else:
            priority = 1.0
        result.append(LangTag(lang, priority))
    result.sort(key=lambda k: k[1], reverse=True)
    return tuple(result)


def parse_accept_lang_header(lang_string: str) -> tuple[LangTag, ...]:
    """
    Parse the value of the Accept-Language header up to a maximum length.

    The value of the header is truncated to a maximum length to avoid potential
    denial of service and memory exhaustion attacks. Excessive memory could be
    used if the raw value is very large as it would be cached due to the use of
    functools.lru_cache() to avoid repetitive parsing of common header values.
    """
    # If the header value doesn't exceed the maximum allowed length, parse it.
    if len(lang_string) <= _ACCEPT_LANGUAGE_HEADER_MAX_LENGTH:
        return _parse_accept_lang_header(lang_string)

    # If there is at least one comma in the value, parse up to the last comma
    # before the max length, skipping any truncated parts at the end of the
    # header value.
    if (index := lang_string.rfind(",", 0, _ACCEPT_LANGUAGE_HEADER_MAX_LENGTH)) > 0:
        return _parse_accept_lang_header(lang_string[:index])

    # Don't attempt to parse if there is only one language-range value which is
    # longer than the maximum allowed length and so truncated.
    return ()
