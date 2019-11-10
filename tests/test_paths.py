import logging

from toolbox import paths

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_path_unicode():
    given = 'AWS Well-Architected Framework \u2013 Operational Excellence Pillar'
    expected = 'AWS Well-Architected Framework - Operational Excellence Pillar'
    assert paths.sanitize_filename(given) == expected


# _____________________________________________________________________________
def test_path_bad_characters():
    given = 'WordPress: Best Practices on AWS'
    expected = 'WordPress- Best Practices on AWS'
    assert paths.sanitize_filename(given) == expected
