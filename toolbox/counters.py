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


# _____________________________________________________________________________
class IncLetterCounter(object):
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


# _____________________________________________________________________________
class AutoId2(object):
    def __init__(self, id1: int = 0, id2: int = 0):
        self._id1 = multiprocessing.Value('i', id1)
        self._id2 = multiprocessing.Value('i', id2)
        self

    def inc1(self):
        with self._id1.get_lock():
            self._id1.value += 1

    def inc2(self):
        with self._id2.get_lock():
            self._id2.value += 1

    @property
    def value(self):
        with self._val.get_lock():
            return self._val.value

    @property
    def inc_id1_value(self):
        with self._val.get_lock():
            self._val.value += 1
            return self._val.value

    @property
    def inc_id2_value(self):
        with self._id2.get_lock():
            self._id2.value += 1
            return self.value
