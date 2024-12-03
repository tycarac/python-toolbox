import logging.config
from pickle import FALSE

import pytest

from toolbox.collectionTools import extract_names, order_names

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ([['c', 'e', 'f'], ['d', 'f'], ['d', 'e'], ['a', 'b', 'f'], ['b', 'c']], ['a', 'b', 'c', 'd', 'e', 'f'])
])
def test_extract_names_1(given, expected):
    assert extract_names(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('names, start, end, expected', [
    (['a', 'b', 'c', 'd', 'e', 'f'], ['d', 'f'], None, ['d', 'f', 'a', 'b', 'c', 'e']),
    (['a', 'b', 'c', 'd', 'e', 'f'], ['e', 'b'], None, ['e', 'b', 'a', 'c', 'd', 'f']),
    (['a', 'b', 'c', 'd', 'e', 'f'], None, ['d', 'b'], ['a', 'c', 'e', 'f', 'd', 'b']),
])
def test_order_names_1(names, start, end, expected):
    assert order_names(names, start, end) == expected

