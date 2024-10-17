from typing import Iterable

"""

References:
1.  Is This the Last Element of My Python for Loop?
    https://medium.com/better-programming/is-this-the-last-element-of-my-python-for-loop-784f5ff90bb5
"""


# _____________________________________________________________________________
def iter_signal_first(it: Iterable[any]) -> Iterable[tuple[bool, any]]:
    iterable = iter(it)
    yield True, next(iterable)
    for val in iterable:
        yield False, val


# _____________________________________________________________________________
def iter_signal_last(it: Iterable[any]) -> Iterable[tuple[bool, any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var
