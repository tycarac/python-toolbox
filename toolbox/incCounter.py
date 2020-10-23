import multiprocessing


# _____________________________________________________________________________
class IncCounter(object):
    def __init__(self, value=0):
        self._val = multiprocessing.Value('i', value)

    def inc(self):
        with self._val.get_lock():
            self._val.value += 1

    @property
    def value(self):
        with self._val.get_lock():
            return self._val.value

    @property
    def inc_value(self):
        with self._val.get_lock():
            self._val.value += 1
            return self._val.value
