"""Testing representing numbers with mextric prefixes

Notes:
    1. Because calculations use floats (real numbers), test data needs to carefully selected to avoid limitations
    of working with floats.  Select test data for expaected comparison and rounding outcomes.  For example,
    round(1.5) may yield value 1 as the underlying float binary value cannot precisely equal a float value.
    https://docs.python.org/3/library/functions.html#round
    https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues
"""
import logging
from toolbox import metricPrefix
import pytest

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (0,        '0'),
    (1,        '1'),
    (999,      '999'),
    (1000,     '1000'),
    (9999,     '9999'),
    (10000,    '10Ki'),
    (10240,    '10Ki'),
    (10700,    '10Ki'),
    (10800,    '11Ki'),
    (100000,   '98Ki'),
    (2**20,    '1024Ki'),
    (2**20*9,  '9216Ki'),
    (2**20*10, '10Mi'),
    (2**20*11, '11Mi')
    ])
def test_to_binary_units(given, expected):
    assert metricPrefix.to_binary_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (2**10*9,   '9216'),
    (2**10*10,  '10Ki'),
    (2**20*9,   '9216Ki'),
    (2**20*10,  '10Mi'),
    (2**30*9,   '9216Mi'),
    (2**30*10,  '10Gi'),
    (2**40*9,   '9216Gi'),
    (2**40*10,  '10Ti'),
    (2**50*9,   '9216Ti'),
    (2**50*10,  '10Pi'),
    (2**60*9,   '9216Pi'),
    (2**60*10,  '10Ei'),
    (2**70*9,   '9216Ei'),
    (2**70*10,  '10Zi'),
    (2**80*9,   '9216Zi'),
    (2**80*10,  '10Yi'),
    (2**80*100, '100Yi')
    ])
def test_to_binary_units_range(given, expected):
    assert metricPrefix.to_binary_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (0,       '0'),
    (1,       '1'),
    (999,     '999'),
    (1000,    '1000'),
    (1024,    '1024'),
    (9999,    '9999'),
    (10000,   '10k'),
    (12345,   '12k'),
    (14400,   '14k'),
    (14600,   '15k'),
    (9400000, '9400k'),
    (9600000, '9600k'),
    (9999400, '9999k'),
    (9999600, '10M')
    ])
def test_to_decimal_units(given, expected):
    assert metricPrefix.to_decimal_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (9999,        '9999'),
    (10**4,       '10k'),
    (10**3*9999,  '9999k'),
    (10**7,       '10M'),
    (10**6*9999,  '9999M'),
    (10**10,      '10G'),
    (10**9*9999,  '9999G'),
    (10**13,      '10T'),
    (10**12*9999, '9999T'),
    (10**16,      '10P'),
    (10**15*9999, '9999P'),
    (10**19,      '10E'),
    (10**18*9999, '9999E'),
    (10**22,      '10Z'),
    (10**21*9999, '9999Z'),
    (10**25,      '10Y'),
    (10**24*9999, '9999Y'),
    (10**28,      '10000Y'),
    (10**29,      '100000Y')
    ])
def test_to_decimal_units_range(given, expected):
    assert metricPrefix.to_decimal_units(given) == expected


