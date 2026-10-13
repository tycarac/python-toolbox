import logging
from pathlib import Path
import pytest

from toolbox import pathTools

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('WordPress:%20Best%20Practices', 'WordPress- Best Practices'),
    ('AWS \u2013 Operational Excellence Pillar', 'AWS - Operational Excellence Pillar'),
    ('AWS Optimizing ASP.NET with C++.pdf', 'AWS Optimizing ASP.NET with C++.pdf'),
    ('', '')
    ])
def test_sanitize_filename(given, expected):
    assert pathTools.sanitize_filename(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('parent, path', [
    (Path('c:\\atemp'), Path('c:\\atemp')),
    (Path('c:\\atemp'), Path('c:\\atemp\\abcd')),
    (Path('e:\\'), Path('e:\\')),
    (Path('c:\\p f\\w nt'), Path('c:\\p f\\w nt\\')),
    (Path('c:\\p f\\w nt'), Path('c:\\p f\\w nt\\s'))
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
    (['abc.net', ''], 'abc.net'),
    (['', ''], '')

])
def test_join_url_path(given, expected):
    assert pathTools.join_urlpath(given[0], *given[1:]) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a', r'a'),
    ('a.b', r'a.b'),
    ('/d/', r'd'),
    ('/a/d/g/', r'a\d\g'),
    ('https://abc.info:80/def/ghi/', r'abc.info\def\ghi'),
    ('//abc.net:81/def/ghi/', r'abc.net\def\ghi'),
    ('/ ec2 /?id = docs_gateway', r'ec2'),
    ('/', ''),
    ('', '')
    ])
def test_urlpath_to_pathname(given, expected):
    assert pathTools.urlpath_to_pathname(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a:80', r'a-80'),
    ('b:80/', r'b-80'),
    ('a.com:80/d/', r'a.com-80\d')
    ])
def test_fail_urlpath_to_pathname(given, expected):
    assert pathTools.urlpath_to_pathname(given) != expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('abc.com', '.com'),
    ('abc.edu/', ''),
    ('abc.org/a.json', '.json'),
    ('abc.info/images.small/i.png', '.png'),
    ('abc.net/p', ''),
    ('abc.org/text.txt/en', ''),
    ('//abc.gov', ''),
    ('//abc.co/', ''),
    ('abc.int/.', ''),
    ('/.', ''),
    ('/.t', '.t'),
    ('/s.t', '.t'),
    ('.txt', '.txt'),
    ('b.html', '.html'),
    ('a.b.xml', '.xml'),
    ('/ ec2 /?id = docs_gateway', ''),
    ('', '')
    ])
def test_url_suffix(given, expected):
    assert pathTools.url_suffix(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('', ''),
    ('.', ''),
    ('..\\', ''),
    ('\\.', ''),
    ('a.e', '.e'),
    ('a.b.e.f', '.f'),
    ('abc.def\\.ext', ''),
    ('abc.def\\g', ''),
    ('abc.def\\g.h', '.h'),
    ('abc.def\\g.hijk', '.hijk'),
    ('abc.def/.ext', ''),
    ('abc.def/ghi', ''),
    ('abc.def/ghi.tar.gzip', '.gzip')
    ])
def test_file_suffix(given, expected):
    assert pathTools.file_suffix(given) == expected
