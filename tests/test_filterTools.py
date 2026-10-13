import logging
import pytest

from toolbox import filterTools

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_sanitize_filename():
    data_1 = ['a.txt', 'b.doc', 'c.docx', 'd.pdf', 'e.bak.txt', 'f.log', 'f.bak.log']
    regex_inc_1 = []
    regex_exc_1 = []
    expected = data_1
    exc_expected = []
    assert filterTools.filter_by_regex(data_1, regex_inc_1, regex_exc_1) == (expected, exc_expected)

