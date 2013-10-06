# -*- coding: UTF-8 -*-
"""
"""
import unittest

from utils import unslugify


class UnSlugifyTest(unittest.TestCase):
    """ unslugify should convert django slugs and with _ to ucfirst words """
    def test_ascii_slug_to_pretty_text(self):
        test = 'my-stupid-monkey'
        expected = 'My stupid monkey'
        result = unslugify(test)
        self.assertEqual(result, expected)

    def test_unicode_slug_to_pretty_text(self):
        test = u'my-stupid-monkey-from-mönchengladbach'
        expected = u'My stupid monkey from mönchengladbach'
        result = unslugify(test)
        self.assertEqual(result, expected)

    def test_unicode_underscores(self):
        test = u'my_stupid_monkey_from_mönchengladbach'
        expected = u'My stupid monkey from mönchengladbach'
        result = unslugify(test)
        self.assertEqual(result, expected)

    def test_unicode_dash_underscores_mixed(self):
        test = u'my_stupid-monkey-from_mönchengladbach'
        expected = u'My stupid monkey from mönchengladbach'
        result = unslugify(test)
        self.assertEqual(result, expected)

    def test_non_slug(self):
        test = u'My stupid monkey from Mönchengladbach'
        expected = u'My stupid monkey from mönchengladbach'
        result = unslugify(test)
        self.assertEqual(result, expected)

    def test_multiple_args_mixed(self):
        test = [u'with-däsh', 'ascii-with-dash', u'with_ünderscore', 'ascii_with_underscore']
        expected = [u'With d\xe4sh', u'Ascii with dash', u'With \xfcnderscore', u'Ascii with underscore']
        result = unslugify(*test)
        self.assertEqual(result, expected)