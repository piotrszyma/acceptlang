import unittest

from acceptlang import parse_accept_lang_header


class ParseTests(unittest.TestCase):

    def test_parse_spec_http_header(self):
        """
        Testing HTTP header parsing. First, we test that we can parse the
        values according to the spec (and that we extract all the pieces in
        the right order).
        """
        tests = [
            # Good headers
            ("de", [("de", 1.0)]),
            ("en-AU", [("en-au", 1.0)]),
            ("es-419", [("es-419", 1.0)]),
            ("*;q=1.00", [("*", 1.0)]),
            ("en-AU;q=0.123", [("en-au", 0.123)]),
            ("en-au;q=0.5", [("en-au", 0.5)]),
            ("en-au;q=1.0", [("en-au", 1.0)]),
            ("da, en-gb;q=0.25, en;q=0.5", [("da", 1.0), ("en", 0.5), ("en-gb", 0.25)]),
            ("en-au-xx", [("en-au-xx", 1.0)]),
            (
                "de,en-au;q=0.75,en-us;q=0.5,en;q=0.25,es;q=0.125,fa;q=0.125",
                [
                    ("de", 1.0),
                    ("en-au", 0.75),
                    ("en-us", 0.5),
                    ("en", 0.25),
                    ("es", 0.125),
                    ("fa", 0.125),
                ],
            ),
            ("*", [("*", 1.0)]),
            ("de;q=0.", [("de", 0.0)]),
            ("en; q=1,", [("en", 1.0)]),
            ("en; q=1.0, * ; q=0.5", [("en", 1.0), ("*", 0.5)]),
            (
                "en" + "-x" * 20,
                [("en-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x", 1.0)],
            ),
            (
                ", ".join(["en; q=1.0"] * 20),
                [("en", 1.0)] * 20,
            ),
            # Bad headers
            ("en-gb;q=1.0000", []),
            ("en;q=0.1234", []),
            ("en;q=.2", []),
            ("abcdefghi-au", []),
            ("**", []),
            ("en,,gb", []),
            ("en-au;q=0.1.0", []),
            (("X" * 97) + "Z,en", []),
            ("da, en-gb;q=0.8, en;q=0.7,#", []),
            ("de;q=2.0", []),
            ("de;q=0.a", []),
            ("12-345", []),
            ("", []),
            ("en;q=1e0", []),
            ("en-au;q=１.０", []),
            # Invalid as language-range value too long.
            ("xxxxxxxx" + "-xxxxxxxx" * 500, []),
            # Header value too long, only parse up to limit.
            (", ".join(["en; q=1.0"] * 500), [("en", 1.0)] * 45),
        ]
        for value, expected in tests:
            with self.subTest(value=value):
                self.assertEqual(parse_accept_lang_header(value), tuple(expected))
