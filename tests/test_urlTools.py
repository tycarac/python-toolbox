import logging
import pytest

from toolbox import urlTools

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a', urlTools.UrlParts('', 'a', '', None, None)),
    ('a.b', urlTools.UrlParts('', 'a.b', '', None, None)),
    ('a.b/', urlTools.UrlParts('', 'a.b', '/', None, None)),
    ('a.b:81', urlTools.UrlParts('', 'a.b:81', '', None, None)),
    ('c@a.b:81', urlTools.UrlParts('', 'c@a.b:81', '', None, None)),
    ('a.b:81/', urlTools.UrlParts('', 'a.b:81', '/', None, None)),
    ('a.b:81/d', urlTools.UrlParts('', 'a.b:81', '/d', None, None)),
    ('a.b:81/d?z=y', urlTools.UrlParts('', 'a.b:81', '/d', 'z=y', None)),
    ('a.b:81/d?z=y#1', urlTools.UrlParts('', 'a.b:81', '/d', 'z=y', '1')),
    ('c@a.b:81/d#1', urlTools.UrlParts('', 'c@a.b:81', '/d', None, '1')),

    ('f:g', urlTools.UrlParts('f', 'g', '', None, None)),
    ('f:g.h', urlTools.UrlParts('f', 'g.h', '', None, None)),
    ('f:g.h/', urlTools.UrlParts('f', 'g.h', '/', None, None)),
    ('f:g.h:81', urlTools.UrlParts('f', 'g.h:81', '', None, None)),
    ('f:i@g.h:81', urlTools.UrlParts('f', 'i@g.h:81', '', None, None)),
    ('f:g.h:81/', urlTools.UrlParts('f', 'g.h:81', '/', None, None)),
    ('f:g.h:81/j', urlTools.UrlParts('f', 'g.h:81', '/j', None, None)),
    ('f:g.h:81/j?z=y', urlTools.UrlParts('f', 'g.h:81', '/j', 'z=y', None)),
    ('f:g.h:81/j?z=y#1', urlTools.UrlParts('f', 'g.h:81', '/j', 'z=y', '1')),
    ('f:i@g.h:81/j#1', urlTools.UrlParts('f', 'i@g.h:81', '/j', None, '1')),

    ('k://l', urlTools.UrlParts('k', 'l', '', None, None)),
    ('k://l.m', urlTools.UrlParts('k', 'l.m', '', None, None)),
    ('k://l.m/', urlTools.UrlParts('k', 'l.m', '/', None, None)),
    ('k://l.m:81', urlTools.UrlParts('k', 'l.m:81', '', None, None)),
    ('k://n@l.m:81', urlTools.UrlParts('k', 'n@l.m:81', '', None, None)),
    ('k://l.m:81/', urlTools.UrlParts('k', 'l.m:81', '/', None, None)),
    ('k://l.m:81/o', urlTools.UrlParts('k', 'l.m:81', '/o', None, None)),
    ('k://l.m:81/o?z=y', urlTools.UrlParts('k', 'l.m:81', '/o', 'z=y', None)),
    ('k://n@l.m:81/o?z=y#1', urlTools.UrlParts('k', 'n@l.m:81', '/o', 'z=y', '1')),
    ('k://n@l.m:81/#1', urlTools.UrlParts('k', 'n@l.m:81', '/', None, '1')),
    ('', urlTools.UrlParts('', '', '', None, None))
    ])
def test_url_split(given, expected):
    assert urlTools.url_split(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a', urlTools.UrlAuthorityParts(None, 'a', None)),
    ('a.b', urlTools.UrlAuthorityParts(None, 'a.b', None)),
    ('a.b:81', urlTools.UrlAuthorityParts(None, 'a.b', 81)),
    ('c@a.b', urlTools.UrlAuthorityParts('c', 'a.b', None)),
    ('c@a.b:81', urlTools.UrlAuthorityParts('c', 'a.b', 81)),
    ('', urlTools.UrlAuthorityParts(None, '', None))
    ])
def test_url_split_authority(given, expected):
    assert urlTools.url_split_authority(given) == expected


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
    assert urlTools.url_split_authority(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (['http://abc.info/', '/def/'], 'http://abc.info/def/'),
    (['http://abc.info/', 'def/'], 'http://abc.info/def/'),
    (['http://abc.info', 'def'], 'http://abc.info/def'),
    (['http://abc.info/', 'def/'], 'http://abc.info/def/'),
    (['http://abc.info/', '/def/'], 'http://abc.info/def/'),
    (['file://abc.org', 'def', 'gh'], 'file://abc.org/def/gh'),
    (['file://abc.org/', '/def/', '/gh/'], 'file://abc.org/def/gh/'),
    (['file://abc.org/', '/def/', '/gh/', '/ij'], 'file://abc.org/def/gh/ij'),
    (['ftps://abc.org', 'def', 'gh', 'ij'], 'ftps://abc.org/def/gh/ij'),
    (['ftps://abc.org', 'def', 'gh', 'ij/'], 'ftps://abc.org/def/gh/ij/'),
    (['abc.edu/', '/'], 'abc.edu/'),
    (['abc.net', ''], 'abc.net/'),
    (['abc.net'], 'abc.net/'),
    (['a', 'b'], 'a/b'),
    (['a', '/b'], 'a/b'),
    (['a', 'b/'], 'a/b/'),
    (['a', '/'], 'a/'),
    (['', '/a/'], '/a/'),
    (['', '/a'], '/a'),
    (['', 'a/'], 'a/'),
    (['', '/'], '/'),
    (['', ' ', ' '], ''),
    (['', '', ''], ''),
    (['', ''], ''),
    ([''], '')
])
def test_url_join(given, expected):
    assert urlTools.url_join(given[0], *given[1:]) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a', r'a'),
    ('a.b', r'a.b'),
    ('/d/', r'd'),
    ('/a/d/g/', r'a\d\g'),
    ('abc.edu:81', r'abc.edu'),
    ('abc.org:80/def/ghi/', r'abc.org\def\ghi'),
    ('https://abc.info:80/def/ghi/', r'abc.info\def\ghi'),
    ('/abc.net:81/def/ghi/', r'abc.net-81\def\ghi'),
    ('/ ec2 /?id = docs_gateway', r'ec2'),
    ('/', ''),
    ('', '')
    ])
def test_url_to_pathname(given, expected):
    assert urlTools.url_to_pathname(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('a:80', r'a-80'),
    ('b:80/', r'b-80'),
    ('a.com:80/d/', r'a.com-80\d')
    ])
def test_fail_url_to_pathname(given, expected):
    assert urlTools.url_to_pathname(given) != expected


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
    assert urlTools.url_path_suffix(given) == expected
