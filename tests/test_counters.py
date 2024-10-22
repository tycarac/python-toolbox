import logging.config

from toolbox.counters import IncCounter, IncLetterCounter

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def test_inc_counter():
    ctr = IncCounter()
    assert ctr.value == 0
    assert ctr.inc_value == 1
    assert ctr.value == 1
    assert ctr.inc_value == 2
    assert ctr.value == 2
    assert ctr.inc_value == 3

    ctr = IncCounter(1)
    assert ctr.value == 1
    assert ctr.inc_value == 2
    assert ctr.inc_value == 3
    assert ctr.inc_value == 4

    ctr = IncCounter(98)
    assert ctr.value == 98
    assert ctr.inc_value == 99
    assert ctr.inc_value == 100
    assert ctr.inc_value == 101
    assert ctr.inc_value == 102


# _____________________________________________________________________________
def test_inc_letter_counter():
    ctr = IncLetterCounter()
    assert ctr.value == 'A'
    assert ctr.inc_value == 'B'
    assert ctr.value == 'B'
    assert ctr.inc_value == 'C'
    assert ctr.value == 'C'
    assert ctr.inc_value == 'D'

    ctr = IncLetterCounter('Y')
    assert ctr.value == 'Y'
    assert ctr.inc_value == 'Z'
    assert ctr.inc_value == 'AA'
    assert ctr.inc_value == 'AB'

    ctr = IncLetterCounter('YY')
    assert ctr.value == 'YY'
    assert ctr.inc_value == 'YZ'
    assert ctr.inc_value == 'ZA'
    assert ctr.inc_value == 'ZB'

    ctr = IncLetterCounter('ZY')
    assert ctr.value == 'ZY'
    assert ctr.inc_value == 'ZZ'
    assert ctr.inc_value == 'AAA'
    assert ctr.inc_value == 'AAB'
    assert ctr.inc_value == 'AAC'

    ctr = IncLetterCounter('BZY')
    assert ctr.value == 'BZY'
    assert ctr.inc_value == 'BZZ'
    assert ctr.inc_value == 'CAA'
    assert ctr.inc_value == 'CAB'
    assert ctr.inc_value == 'CAC'
