"""Testing representing numbers with mextric prefixes

Notes:
    1. Because calculations use floats (real numbers), test data needs to carefully selected to avoid limitations
    of working with floats.  Select test data for expaected comparison and rounding outcomes.  For example,
    round(1.5) may yield value 1 as the underlying float binary value cannot precisely equal a float value.
    https://docs.python.org/3/library/functions.html#round
    https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues
"""
import logging
import metricPrefix
import pytest

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (0, ('0', '')),
    (1, ('1', '')),
    (999, ('999', '')),
    (1000, ('1000', '')),
    (9999, ('9999', '')),
    (10000, ('10', 'Ki')),
    (10240, ('10', 'Ki')),
    (10700, ('10', 'Ki')),
    (10800, ('11', 'Ki')),
    (100000, ('98', 'Ki')),
    (2**20, ('1024', 'Ki')),
    (2**20*9, ('9216', 'Ki')),
    (2**20*10, ('10', 'Mi')),
    (2**20*11, ('11', 'Mi'))
    ])
def test_to_binary_units(given, expected):
    assert metricPrefix.to_binary_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (2**10*9,   ('9216', '')),
    (2**10*10,  ('10', 'Ki')),
    (2**20*9,   ('9216', 'Ki')),
    (2**20*10,  ('10', 'Mi')),
    (2**30*9,   ('9216', 'Mi')),
    (2**30*10,  ('10', 'Gi')),
    (2**40*9,   ('9216', 'Gi')),
    (2**40*10,  ('10', 'Ti')),
    (2**50*9,   ('9216', 'Ti')),
    (2**50*10,  ('10', 'Pi')),
    (2**60*9,   ('9216', 'Pi')),
    (2**60*10,  ('10', 'Ei')),
    (2**70*9,   ('9216', 'Ei')),
    (2**70*10,  ('10', 'Zi')),
    (2**80*9,   ('9216', 'Zi')),
    (2**80*10,  ('10', 'Yi')),
    (2**80*100, ('100', 'Yi'))
    ])
def test_to_binary_units_range(given, expected):
    assert metricPrefix.to_binary_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (0, ('0', '')),
    (1, ('1', '')),
    (999, ('999', '')),
    (1000, ('1000', '')),
    (1024, ('1024', '')),
    (9999, ('9999', '')),
    (10000, ('10', 'k')),
    (12345, ('12', 'k')),
    (14400, ('14', 'k')),
    (14600, ('15', 'k')),
    (9400000, ('9400', 'k')),
    (9600000, ('9600', 'k')),
    (9999400, ('9999', 'k')),
    (9999600, ('10', 'M'))
    ])
def test_to_decimal_units(given, expected):
    assert metricPrefix.to_decimal_units(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (9999,        ('9999', '')),
    (10**4,       ('10', 'k')),
    (10**3*9999,  ('9999', 'k')),
    (10**7,       ('10', 'M')),
    (10**6*9999,  ('9999', 'M')),
    (10**10,      ('10', 'G')),
    (10**9*9999,  ('9999', 'G')),
    (10**13,      ('10', 'T')),
    (10**12*9999, ('9999', 'T')),
    (10**16,      ('10', 'P')),
    (10**15*9999, ('9999', 'P')),
    (10**19,      ('10', 'E')),
    (10**18*9999, ('9999', 'E')),
    (10**22,      ('10', 'Z')),
    (10**21*9999, ('9999', 'Z')),
    (10**25,      ('10', 'Y')),
    (10**24*9999, ('9999', 'Y')),
    (10**28,      ('10000', 'Y')),
    (10**29,      ('100000', 'Y'))
    ])
def test_to_decimal_units_range(given, expected):
    assert metricPrefix.to_decimal_units(given) == expected


