import logging
from pathlib import Path
import pytest

from toolbox import filterTools

logger = logging.getLogger(__name__)
data_1 = ['a.txt', 'b.doc', 'c.docx', 'd.pdf', 'e.bak.txt', 'f.log', 'f.bak.log', 'g.txt', 'g.txt.bak']
data_2 = ['a.py', 'b.py', 'ab.py', 'bb.py', 'bb.bak.py', 'aa.py', 'ac.py']


# _____________________________________________________________________________
def test_filter_paths_by_regex_1():
    path = Path(r'..\tests\data')

    regex_inc = [r'\.json$']
    regex_exc = [r'\.bak(?:\.\w+)*$']
    results = list(filterTools.filter_paths_by_regex(path, regex_inc, regex_exc))

    path = path.resolve()
    results_relative = list(map(lambda x: x.relative_to(path), results))
    assert results_relative == [Path('data-arrays.json'), Path('data-books.json'), Path('data-types.json')]


# _____________________________________________________________________________
def test_filter_paths_by_regex_2():
    path = Path(r'..\tests\data')

    regex_exc = [r'\.json$$|\.back$']
    results = list(filterTools.filter_paths_by_regex(path, None, regex_exc))

    path = path.resolve()
    results_relative = list(map(lambda x: x.relative_to(path), results))
    assert results_relative == [Path('record.csv')]


# _____________________________________________________________________________
def test_filter_by_regex_null():

    # Empty regrex
    result = list(filterTools.filter_by_regex(data_1, None, None))
    assert result == data_1
    result = list(filterTools.filter_by_regex(data_1, [], []))
    assert result == data_1

    # No match regex
    regex_inc = [r'\w+(?:\.\w+)']
    regex_exc = [r'.*\.[\.bak|\.wbk]$']
    result = list(filterTools.filter_by_regex(data_1, regex_inc, regex_exc))
    assert result == data_1


# _____________________________________________________________________________
def test_filter_by_regex():
    regex_exc = [r'\.bak(?:\.\w+)*$']
    result = list(filterTools.filter_by_regex(data_1, [], regex_exc))
    assert result == ['a.txt', 'b.doc', 'c.docx', 'd.pdf', 'f.log', 'g.txt']

    regex_inc = [r'\.txt$']
    result = list(filterTools.filter_by_regex(data_1, regex_inc, []))
    assert result == ['a.txt', 'e.bak.txt', 'g.txt']

    result = list(filterTools.filter_by_regex(data_1, regex_inc, regex_exc))
    assert result == ['a.txt', 'g.txt']

