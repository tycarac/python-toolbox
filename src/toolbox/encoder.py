from hashlib import blake2b
from sys import byteorder


# _____________________________________________________________________________
class CharSetEncoder:
    _CHAR_SET = '0123456789bcdfghjkmnpqrstvwxyz'
    _HASH_DIGEST_SIZE = 6
    _char_set: str
    _char_set_len: int
    _hash_digest_size: int

    def __init__(self, char_set: str = _CHAR_SET, hash_digest_size: int = _HASH_DIGEST_SIZE):
        if char_set is None or len(char_set) < 2:
            raise ValueError('char_set must have at least 2 characters')
        self._char_set = char_set
        self._char_set_len = len(char_set)
        self._hash_digest_size = hash_digest_size

    def hash(self, string: str) -> str:
        return self.encode(
            int.from_bytes(blake2b(bytearray(string, 'utf-8'), digest_size=self._hash_digest_size).digest(),
                           byteorder=byteorder))

    def encode(self, number: int) -> str:
        if number < 0:
            raise ValueError('number cannot be negative')
        if number == 0:
            return self._char_set[0]
        string = ''
        while number != 0:
            number, rem = divmod(number, self._char_set_len)
            string += self._char_set[rem]
        return string

    def decode(self, string: str) -> int:
        number = 0
        for ch in string[::-1]:
            number = number * self._char_set_len + self._char_set.index(ch)
        return number
