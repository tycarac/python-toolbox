import logging
import pytest

from toolbox.iterTools import iter_signal_first, iter_signal_last

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_iter_signal_first():
    itr = iter_signal_first([1, 2, 3])
    assert(next(itr) == (True, 1))
    assert(next(itr) == (False, 2))
    assert(next(itr) == (False, 3))
    with pytest.raises(StopIteration):
        next(itr)


# _____________________________________________________________________________
def test_iter_signal_last():
    itr = iter_signal_last([1, 2, 3])
    assert(next(itr) == (False, 1))
    assert(next(itr) == (False, 2))
    assert(next(itr) == (True, 3))
    with pytest.raises(StopIteration):
        next(itr)

