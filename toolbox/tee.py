from pathlib import Path
import sys


class Tee(object):
    def __init__(self, filename=None, mode='wt', flush=True):
        if filename is None:
            filename = Path(sys.argv[0]).stem + '.tee.log'
        self.filename = filename
        self.file = open(filename, mode, flush)
        self.stdout = sys.stdout
        sys.stdout = self
        self.stderr = sys.stderr
        sys.stderr = self

    def __enter__(self):
        pass

    def __del__(self):
        self.close()

    def __exit__(self, *args):
        self.close()

    def write(self, data):
        if self.file:
            self.file.write(data)
            self.file.flush()
        self.stdout.write(data)
        sys.stdout.flush()

    def flush(self):
        self.file.flush()

    def close(self):
        if self.file:
            try:
                self.file.close()
            finally:
                self.file = None
                sys.stdout = self.stdout
                sys.stderr = self.stderr
