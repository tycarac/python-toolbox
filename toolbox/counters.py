import multiprocessing
from typing import List
import re

re_letter_number = re.compile(r'\s*([A-Z]+)([0-9]+)\s*')

# _____________________________________________________________________________
class IncCounter(object):
    def __init__(self, value=0):
        self._val = multiprocessing.Value('i', value)

    def inc(self) -> None:
        with self._val.get_lock():
            self._val.value += 1

    @property
    def value(self) -> int:
        with self._val.get_lock():
            return self._val.value

    @property
    def inc_value(self) -> int:
        with self._val.get_lock():
            self._val.value += 1
            return self._val.value


# _____________________________________________________________________________
class IncLetterCounter(object):
    _arr: List[int]
    _value: str

    def __init__(self, init_value: str = 'A'):
        self._value = init_value.upper()
        self._arr = list(ord(c) for c in reversed(self._value))

    def inc(self) -> None:
        self._arr[0] += 1
        if (l := len(self._arr)) == 1 and (c := self._arr[0]) <= 90:
            self._value = chr(c)
        else:
            for i in range(l - 1):
                if self._arr[i] > 90:
                    self._arr[i] = 65
                    self._arr[i + 1] += 1
            if self._arr[-1] > 90:
                self._arr[-1] = 65
                self._arr.append(65)
            self._value = ''.join(chr(x) for x in reversed(self._arr))

    @property
    def value(self) -> str:
        return self._value

    @property
    def inc_value(self) -> str:
        self.inc()
        return self._value

# _____________________________________________________________________________
class IncLetterNumberCounter(object):
    _arr: List[int]
    _number: int
    _str : str
    _value: str

    def __init__(self, init_value: str = 'A1'):
        if not (matches := re_letter_number.match(init_value.upper())):
            raise RuntimeError(f'Not valid input: "{init_value}"')
        self._str = matches[1]
        self._number = int(matches[2])
        self._value = self._str + str(self._number)
        self._arr = list(ord(c) for c in reversed(self._str))

    @property
    def inc_letter_value(self) -> str:
        self._arr[0] += 1
        if (l := len(self._arr)) == 1 and (c := self._arr[0]) <= 90:
            self._str = chr(c)
        else:
            for i in range(l - 1):
                if self._arr[i] > 90:
                    self._arr[i] = 65
                    self._arr[i + 1] += 1
            if self._arr[-1] > 90:
                self._arr[-1] = 65
                self._arr.append(65)
            self._str = ''.join(chr(x) for x in reversed(self._arr))
        self._value = self._str + str(self._number)
        return self._value

    @property
    def inc_number_value(self) -> str:
        self._number += 1
        self._value = self._str + str(self._number)
        return self._value

    @property
    def value(self) -> str:
        return self._value

