#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

# Allow direct execution
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from youtube_dl.utils import get_filesystem_encoding
from youtube_dl.compat import (
    compat_getenv,
    compat_etree_fromstring,
    compat_expanduser,
    compat_shlex_split,
    compat_str,
    compat_urllib_parse_unquote,
    compat_urllib_parse_unquote_plus,
    compat_urllib_parse_urlencode,
)


class TestCompat(unittest.TestCase):
    def test_compat_getenv(self):
        test_str = 'тест'
        os.environ['YOUTUBE-DL-TEST'] = (
            test_str if sys.version_info >= (3, 0)
            else test_str.encode(get_filesystem_encoding()))
        self.assertEqual(compat_getenv('YOUTUBE-DL-TEST'), test_str)

    def test_compat_expanduser(self):
        old_home = os.environ.get('HOME')
        test_str = 'C:\Documents and Settings\тест\Application Data'
        os.environ['HOME'] = (
            test_str if sys.version_info >= (3, 0)
            else test_str.encode(get_filesystem_encoding()))
        self.assertEqual(compat_expanduser('~'), test_str)
        os.environ['HOME'] = old_home

    def test_all_present(self):
        import youtube_dl.compat
        all_names = youtube_dl.compat.__all__
        present_names = set(filter(
            lambda c: '_' in c and not c.startswith('_'),
            dir(youtube_dl.compat))) - set(['unicode_literals'])
        self.assertEqual(all_names, sorted(present_names))

    def test_compat_urllib_parse_unquote(self):
        self.assertEqual(compat_urllib_parse_unquote('abc%20def'), 'abc def')
        self.assertEqual(compat_urllib_parse_unquote('%7e/abc+def'), '~/abc+def')
        self.assertEqual(compat_urllib_parse_unquote(''), '')
        self.assertEqual(compat_urllib_parse_unquote('%'), '%')
        self.assertEqual(compat_urllib_parse_unquote('%%'), '%%')
        self.assertEqual(compat_urllib_parse_unquote('%%%'), '%%%')
        self.assertEqual(compat_urllib_parse_unquote('%2F'), '/')
        self.assertEqual(compat_urllib_parse_unquote('%2f'), '/')
        self.assertEqual(compat_urllib_parse_unquote('%E6%B4%A5%E6%B3%A2'), '津波')
        self.assertEqual(
            compat_urllib_parse_unquote('''<meta property="og:description" content="%E2%96%81%E2%96%82%E2%96%83%E2%96%84%25%E2%96%85%E2%96%86%E2%96%87%E2%96%88" />
%<a href="https://ar.wikipedia.org/wiki/%D8%AA%D8%B3%D9%88%D9%86%D8%A7%D9%85%D9%8A">%a'''),
            '''<meta property="og:description" content="▁▂▃▄%▅▆▇█" />
%<a href="https://ar.wikipedia.org/wiki/تسونامي">%a''')
        self.assertEqual(
            compat_urllib_parse_unquote('''%28%5E%E2%97%A3_%E2%97%A2%5E%29%E3%81%A3%EF%B8%BB%E3%83%87%E2%95%90%E4%B8%80    %E2%87%80    %E2%87%80    %E2%87%80    %E2%87%80    %E2%87%80    %E2%86%B6%I%Break%25Things%'''),
            '''(^◣_◢^)っ︻デ═一    ⇀    ⇀    ⇀    ⇀    ⇀    ↶%I%Break%Things%''')

    def test_compat_urllib_parse_unquote_plus(self):
        self.assertEqual(compat_urllib_parse_unquote_plus('abc%20def'), 'abc def')
        self.assertEqual(compat_urllib_parse_unquote_plus('%7e/abc+def'), '~/abc def')

    def test_compat_urllib_parse_urlencode(self):
        self.assertEqual(compat_urllib_parse_urlencode({'abc': 'def'}), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode({'abc': b'def'}), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode({b'abc': 'def'}), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode({b'abc': b'def'}), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode([('abc', 'def')]), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode([('abc', b'def')]), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode([(b'abc', 'def')]), 'abc=def')
        self.assertEqual(compat_urllib_parse_urlencode([(b'abc', b'def')]), 'abc=def')

    def test_compat_shlex_split(self):
        self.assertEqual(compat_shlex_split('-option "one two"'), ['-option', 'one two'])

    def test_compat_etree_fromstring(self):
        xml = '''
            <root foo="bar" spam="中文">
                <normal>foo</normal>
                <chinese>中文</chinese>
                <foo><bar>spam</bar></foo>
            </root>
        '''
        doc = compat_etree_fromstring(xml.encode('utf-8'))
        self.assertTrue(isinstance(doc.attrib['foo'], compat_str))
        self.assertTrue(isinstance(doc.attrib['spam'], compat_str))
        self.assertTrue(isinstance(doc.find('normal').text, compat_str))
        self.assertTrue(isinstance(doc.find('chinese').text, compat_str))
        self.assertTrue(isinstance(doc.find('foo/bar').text, compat_str))

if __name__ == '__main__':
    unittest.main()
