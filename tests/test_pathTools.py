import logging
from pathlib import Path
import pytest

from toolbox import pathTools

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('WordPress: Best Practices', 'WordPress- Best Practices'),
    ('AWS \u2013 Operational Excellence Pillar', 'AWS - Operational Excellence Pillar'),
    ('AWS Optimizing ASP.NET with C++.pdf', 'AWS Optimizing ASP.NET with C++.pdf')
    ])
def test_sanitize_filename(given, expected):
    assert pathTools.sanitize_filename(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('parent, path', [
    (Path('c:\\atemp'), Path('c:\\atemp')),
    (Path('c:\\atemp'), Path('c:\\atemp\\abcd')),
    (Path('e:\\'), Path('e:\\'))
    ])
def test_is_parent_path(parent, path):
    assert pathTools.is_parent(parent, path)


# _____________________________________________________________________________
@pytest.mark.parametrize('parent, path',
    [(Path('c:\\abcd\\efgh'), Path('c:\\temp\\efgh')),
    (Path('e:\\'), Path('f:\\'))
    ])
def test_fail_is_parent_path(parent, path):
    assert not pathTools.is_parent(parent, path)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (['https://abc.info/', '/def/'], 'https://abc.info/def'),
    (['https://abc.org/', '/def/', '/gh/'], 'https://abc.org/def/gh'),
    (['ftps://abc.int', 'def', 'gh'], 'ftps://abc.int/def/gh'),
    (['abc.co.uk/', '/d/', '/g/'], 'abc.co.uk/d/g'),
    (['abc.edu/', '/'], 'abc.edu'),
    (['abc.net', ''], 'abc.net')
    ])
def test_join_url_path(given, expected):
    assert pathTools.join_urlpath(given[0], *given[1:]) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('//abc/', r'abc'),
    ('/ ec2 /?id = docs_gateway', r'ec2'),
    ('a', r'a'),
    ('a.b', r'a.b'),
    ('/abc/def/ghi/', r'abc\def\ghi'),
    ('https://abc.info:80/def/ghi/', r'abc.info\def\ghi')
    ])
def test_urlpath_to_pathname(given, expected):
    assert pathTools.urlpath_to_pathname(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('abc.org/a.json', '.json'),
    ('abc.info/images.small/i.png', '.png'),
    ('abc.org/text.txt/en', ''),
    ('abc.net/page', ''),
    ('abc.com', '.com'),
    ('//abc.gov', ''),
    ('abc.edu/', ''),
    ('abc.int/.', ''),
    ('.txt', '.txt'),
    ('b.html', '.html'),
    ('a.b.xml', '.xml'),
    ('/ ec2 /?id = docs_gateway', ''),
    ])
def test_url_suffix(given, expected):
    assert pathTools.url_suffix(given) == expected

