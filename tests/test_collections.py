import logging.config

import pytest

from toolbox.collectionTools import extract_names

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ([['c', 'e', 'f'], ['d', 'f'], ['d', 'e'], ['a', 'b', 'f'], ['b', 'c']], ['a', 'b', 'c', 'd', 'e', 'f'])])
def test_extract_names_1(given, expected):
    assert extract_names(given) == expected
