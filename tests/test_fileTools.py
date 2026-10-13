import logging
from pathlib import Path
import pytest

from resources import fileTools

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('WordPress:%20Best%20Practices', 'WordPress- Best Practices'),
    ('AWS \u2013 Operational Excellence Pillar', 'AWS - Operational Excellence Pillar'),
    ('AWS Optimizing ASP.NET with C++.pdf', 'AWS Optimizing ASP.NET with C++.pdf'),
    ('  AWS    Security   Best    Practices  ', 'AWS Security Best Practices'),  # Test multiple spaces
    ('-\u2012\u2013\u2014\u2015\u2053', '------'),
    ('.a.b.c.d', '.a.b.c.d'),
    ('\t', ''),
    ('', '')
    ])
def test_sanitize_filepath(given, expected):
    assert fileTools.sanitize_filepath(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('.', '.'),
    ('.a', '.a'),
    ('..a', '.-a'),
    ('.a.txt', '.a-txt'),
    ('b', 'b'),
    ('b.txt', 'b-txt'),
    ('b.bak.txt', 'b-bak-txt'),
    ('c.', 'c-'),
    ('No. 11', 'No- 11'),
    ('.a.b.c.d', '.a-b-c-d'),
    ('', ''),
    ('\t', '')
    ])
def test_dot_sanitize_filepath(given, expected):
    assert fileTools.sanitize_filepath(given, replace_dot=True) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('c:\\', 'c--'),
    ('\\a\\b\\', '-a-b-'),
    ('/c/d/', '-c-d-'),
    ('file://e/f/', 'file---e-f-'),
    ('', ''),
    ('\t', '')
    ])
def test_sep_sanitize_filename(given, expected):
    assert fileTools.sanitize_filepath(given, replace_folder_sep=True) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('parent, path', [
    (Path('c:\\atemp'), Path('c:\\atemp')),
    (Path('c:\\atemp'), Path('c:\\atemp\\abcd')),
    (Path('e:\\'), Path('e:\\')),
    (Path('c:\\p f\\w nt'), Path('c:\\p f\\w nt\\')),
    (Path('c:\\p f\\w nt'), Path('c:\\p f\\w nt\\s.txt'))
    ])
def test_is_parent_path(parent, path):
    assert fileTools.is_parent(parent, path)


# _____________________________________________________________________________
@pytest.mark.parametrize('parent, path', [
    (Path('c:\\abcd\\efgh'), Path('c:\\temp\\efgh')),
    (Path('e:\\'), Path('f:\\'))
    ])
def test_fail_is_parent_path(parent, path):
    assert not fileTools.is_parent(parent, path)


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
    assert fileTools.file_suffix(given) == expected
