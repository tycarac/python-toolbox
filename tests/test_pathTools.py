import logging
from pathlib import Path
from toolbox import pathTools

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_sanitize_filename():
    pos_tests = [
        ['WordPress- Best Practices', 'WordPress: Best Practices'],
        ['AWS - Operational Excellence Pillar', 'AWS \u2013 Operational Excellence Pillar'],
        ['AWS Optimizing ASP.NET with C++.pdf', 'AWS Optimizing ASP.NET with C++.pdf']
    ]

    for test in pos_tests:
        expected, given = test
        assert expected == pathTools.sanitize_filename(given)


# _____________________________________________________________________________
def test_is_parent_path():
    pos_tests = [
        [Path('c:\\atemp'), Path('c:\\atemp')],
        [Path('c:\\atemp'), Path('c:\\atemp\\abcd')]
    ]
    neg_tests = [
        [Path('c:\\abcd\\abcd'), Path('c:\\temp\\abcd')]
    ]

    for test in pos_tests:
        parent, path = test
        assert pathTools.is_parent(parent, path)
    for test in neg_tests:
        parent, path = test
        assert not pathTools.is_parent(parent, path)


# _____________________________________________________________________________
def test_join_url_path():
    def func(url, args):
        return pathTools.join_url_path(url, *args)

    pos_tests = [
        ['https://abc.com/def', ['https://abc.com/', '/def/']],
        ['https://abc.com/def/ghi', ['https://abc.com/', '/def/', '/ghi/']],
        ['abc.com/def/ghi', ['abc.com/', '/def/', '/ghi/']]
    ]

    for test in pos_tests:
        expected, given = test
        assert expected == func(given[0], given[1:])


# _____________________________________________________________________________
def test_urlpath_to_pathname():
    pos_tests = [
        [r'abc', '//abc/'],
        [r'abc\def\ghi', '/abc/def/ghi/'],
        [r'ec2', '/ ec2 /?id = docs_gateway']
    ]

    for test in pos_tests:
        expected, given = test
        assert expected == pathTools.urlpath_to_pathname(given)

