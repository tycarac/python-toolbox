import os.path
import re
from pathlib import Path
from typing import Iterable


# _____________________________________________________________________________
def filter_paths_by_regex(path: os.PathLike, inc_regexes: list[str] = None, exc_regexes: list[str] = None,
                          file_filter: str = '*.*'):
    """Use recursive glob to collect the files in a named path and then apply regex include and exclude filters.

    Notes:
        1. Prefilter can be applied to glob function to reduce size of data processed
        2. Regex expressions only applied to filename and not path (Use of dict).
    :param path:
    :param file_filter: glob
    :param inc_regexes:
    :param exc_regexes:
    :return: iterator of applied filters
    """
    inc_cmpl = [re.compile(regex, re.IGNORECASE) for regex in inc_regexes] if inc_regexes else None
    exc_cmpl = [re.compile(regex, re.IGNORECASE) for regex in exc_regexes] if exc_regexes else None

    for p in Path(path).resolve().rglob(file_filter):
        if (not inc_cmpl or any(r.search(p.name) for r in inc_cmpl)) \
                and not (exc_cmpl and any(r.search(p.name) for r in exc_cmpl)):
            yield p


# _____________________________________________________________________________
def filter_by_regex(itr: Iterable, inc_regexes: list[str] = None, exc_regexes: list[str] = None):
    """Filter the input iterable against two lists of regex (regular expressions).

    First, keep collection items with any regex match in the include regex list.  Then second, remove
    collection items with any regex match in the exclude regex list.

    Notes:
    1. Using iterators frees fuction to work with different collection types
    2. Reference to input collection is returned, not a copy, if there are no input filters
    3. Either or both regex lists can be null or empty
    4. Regex expressions are compiled to ignore case and compilations are not cached
    :param itr: iterator input to be filtered
    :param inc_regexes:
    :param exc_regexes:
    :return: iterator of applied filters
    """
    inc_cmpl = [re.compile(regex, re.IGNORECASE) for regex in inc_regexes] if inc_regexes else None
    exc_cmpl = [re.compile(regex, re.IGNORECASE) for regex in exc_regexes] if exc_regexes else None

    if inc_cmpl and exc_cmpl:
        fitr = filter(lambda x: (any(r.search(x) for r in inc_cmpl) and not (any(r.search(x) for r in exc_cmpl))), itr)
    elif inc_cmpl:
        fitr = filter(lambda x: any(r.search(x) for r in inc_cmpl), itr)
    elif exc_cmpl:
        fitr = filter(lambda x: not any(r.search(x) for r in exc_cmpl), itr)
    else:
        fitr = itr

    for x in fitr:
        yield x
