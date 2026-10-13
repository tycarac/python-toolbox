import logging
from pathlib import Path
from toolbox import paths as p

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_path_unicode():
    given = 'AWS Well-Architected Framework \u2013 Operational Excellence Pillar'
    expected = 'AWS Well-Architected Framework - Operational Excellence Pillar'
    assert p.sanitize_filename(given) == expected


# _____________________________________________________________________________
def test_path_bad_characters():
    given = 'WordPress: Best Practices on AWS'
    expected = 'WordPress- Best Practices on AWS'
    assert p.sanitize_filename(given) == expected


# _____________________________________________________________________________
def test_is_parent_path():
    tests = [
        [Path('c:\\atemp'), Path('c:\\atemp'), True],
        [Path('c:\\atemp'), Path('c:\\atemp\\abcd'), True],
        [Path('c:\\abcd\\abcd'), Path('c:\\temp\\abcd'), False]
    ]

    for test in tests:
        p1, p2, result = test
        assert p.is_parent(p1, p2) == result
