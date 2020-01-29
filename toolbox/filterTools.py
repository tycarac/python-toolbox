from pathlib import Path
import re
import os.path
from typing import List, Set, Any


# _____________________________________________________________________________
def filter_paths_by_regex(directory: os.PathLike,
            file_pattern:str = None, inc_regex_str: List[str] = None, exc_regex_str: List[str] = None):
    file_filter = file_pattern if not None else '*.*'
    paths = {p.name: p for p in Path(directory).rglob(file_filter)}
    return filter_by_regex(paths, inc_regex_str, exc_regex_str)


# _____________________________________________________________________________
def filter_by_regex(collect: List[Any] or Set[Any], inc_regex_str: List[str] = None, exc_regex_str: List[str] = None):
    if inc_regex_str:
        inc_regex = [re.compile(regex, re.IGNORECASE) for regex in inc_regex_str]
        inc_collect = [p for p in collect if any(r.match(p) for r in inc_regex)]
    else:
        inc_collect = collect

    if exc_regex_str:
        exc_regex = [re.compile(regex, re.IGNORECASE) for regex in exc_regex_str]
        exc_collect = sorted([p for p in inc_collect if any(r.match(p.name) for r in exc_regex)])
    else:
        exc_collect = []

    out_collect = [p1 for p1 in inc_collect if p1 not in exc_collect]
    return out_collect, exc_collect
