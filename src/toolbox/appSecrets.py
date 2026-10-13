"""
Load secrets file using best practices for Linux
  - Pass only value of named secret.  Do not pass secrets as a collection.
  - Do not hold secrets in memory longer than needed.
    - Do not assign to static variable.  Files typically cached by OS anyway.
Improvements:
 - Overwrite memory after use
"""
import logging.handlers
from pathlib import Path

# Common variables
_logger = logging.getLogger(__name__)
_SECRETS_FILE = Path(Path.home(), '.secrets', 'trades').resolve()


# _____________________________________________________________________________
def _load_secrets(name: str, path: Path = _SECRETS_FILE) -> str:
    if not path.is_file():
        raise FileNotFoundError(f'Secrets file not found: "{path}"')
    with path.open("rt", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            if (line := raw_line.strip()) and line[0] != '#':
                try:
                    key, value = line.split('=', maxsplit=1)
                except ValueError as ex:
                    raise ValueError(f'Invalid secret at "{path}:{line_number}"') from ex
                if not (key := key.strip()):
                    raise ValueError(f'Empty secret name at "{path}:{line_number}"')
                elif name == key:
                    return value.strip()
    return ''


# _____________________________________________________________________________
def get_secret(name: str) -> str:
    if name and (n := name.strip()) and (s := _load_secrets(n)):
        return s
    else:
        raise KeyError(f'Secret "{name}" not found in "{_SECRETS_FILE}"')
