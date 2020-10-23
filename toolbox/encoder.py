from hashlib import blake2b
from sys import byteorder


# _____________________________________________________________________________
class CharSetEncoder:
    _char_set = '0123456789bcdfghjkmnpqrstvwxyz'

    def __init__(self, digest_size=4, char_set=None):
        self._char_set = char_set if char_set else CharSetEncoder._char_set
        self._digest_size = digest_size
        self._base = len(self._char_set)

    def hash(self, string: str) -> str:
        return self.encode(int.from_bytes(blake2b(bytearray(string, 'utf-8'), digest_size=self._digest_size).digest(),
                                          byteorder=byteorder))

    def encode(self, number: int) -> str:
        if number < 0:
            raise ValueError('number cannot be negative')
        if number == 0:
            return self._char_set[0]
        string = ''
        while number != 0:
            number, rem = divmod(number, self._base)
            string += self._char_set[rem]
        return string

    def decode(self, string: str) -> int:
        number = 0
        for ch in string[::-1]:
            number = number * self._base + self._char_set.index(ch)
        return number
