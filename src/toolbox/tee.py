import sys
from pathlib import Path
from typing import Any, IO


# _____________________________________________________________________________
class Tee(object):
    def __init__(self, filename=None, mode: str = 'wt', flush: bool = True) -> None:
        self.filename = filename if filename else Path(sys.argv[0]).stem + '.tee.log'
        self.file = open(filename, mode, flush)
        self.stdout = sys.stdout
        sys.stdout = self
        self.stderr = sys.stderr
        sys.stderr = self

    def __enter__(self) -> None:
        pass

    def __del__(self) -> None:
        self.close()

    def __exit__(self, *args: Any) -> None:
        self.close()

    def write(self, data: IO[bytes]) -> None:
        if self.file:
            self.file.write(data)
            self.file.flush()
        self.stdout.write(data)
        sys.stdout.flush()

    def flush(self) -> None:
        self.file.flush()

    def close(self) -> None:
        if self.file:
            try:
                self.file.close()
            finally:
                self.file = None
                sys.stdout = self.stdout
                sys.stderr = self.stderr
