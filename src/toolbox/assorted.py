import logging.config
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal
from html import escape
from pathlib import Path
from string.templatelib import Template
from typing import Any, Final, TypeVar

_logger = logging.getLogger(__name__)
T = TypeVar('T')
MONTHS: Final[dict[str, int]] = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
                                 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12, }
CSV_BACKUP_SUFFIX = '.bak.csv'


# _____________________________________________________________________________
def str_to_bool(s: str | bool | None) -> bool:
    return s.lower() in ('true', 't', 'yes', '1') if type(s) is str else bool(s)


# _____________________________________________________________________________
def is_blank(s: str) -> bool:
    return not bool(s and s.strip())


# _____________________________________________________________________________
def is_not_blank(s: str) -> bool:
    return bool(s and s.strip())


# _____________________________________________________________________________
def normalize_blank(s: str) -> str:
    return ' '.join(s.split()) if s else ''


# _____________________________________________________________________________
def str_to_decimal(s: str) -> Decimal:
    return Decimal(s) if (s and s.strip()) else Decimal('0.0')


# _____________________________________________________________________________
def format_amount(d: Decimal) -> str:
    return f'{d:.3f}' if (d < 2.00) else f'{d:.2f}'


# _____________________________________________________________________________
def real_to_str(v: float | Decimal) -> str:
    return f'{v:.5f}'.rstrip('0').rstrip('.')


# _____________________________________________________________________________
def date_to_tax_year(d: date | datetime) -> str:
    return f'FY{(d.year if (d.month <= 6) else d.year + 1) % 100}'


# _____________________________________________________________________________
def shorten_path(path: Path | str) -> Path | str:
    try:
        if type(path) is Path:
            return Path('~', path.relative_to(Path.home()))
        else:
            return str(Path('~/', Path(path).relative_to(Path.home())))
    except ValueError:
        return path


# _____________________________________________________________________________
def multisort[T](coll: list[T], specs: list[tuple[Callable[[T], Any], bool]]) -> list[T]:
    for key, reverse in reversed(specs):
        coll.sort(key=key, reverse=reverse)
    return coll


# _____________________________________________________________________________
def backup_file(file: Path) -> None:
    if file.exists():
        backup_folder: Path = Path(file.parent, 'backup').resolve()
        backup_folder.mkdir(parents=True, exist_ok=True)

        backup_filepath: Path = Path(backup_folder, file.with_suffix(CSV_BACKUP_SUFFIX).name).resolve()
        _logger.debug(f'backup file: "{backup_filepath}"')
        try:
            backup_filepath.write_text(file.read_text())
        except Exception:
            _logger.exception(f'Error backing up data file: "{backup_filepath}"')


# _____________________________________________________________________________
def tsql(template: Template) -> tuple[str, list]:
    """
    Safely insert and sanitize parameters to be inserted into parameterized SQL using t-strings.
    :param template: SQL template
    :return:
    """
    parts: list[str] = []
    params: list[str] = []
    for t in template:
        if isinstance(t, str):
            parts.append(t)
        else:
            parts.append('?')
            params.append(t.value)
    return ''.join(parts), params


# _____________________________________________________________________________
def thtml(template: Template) -> str:
    """
    Safely insert and sanitize parameters to be inserted into parameterized HTML using t-strings.
    :param template: HTML template
    :return:
    """
    parts: list[str] = []
    for t in template:
        parts.append(t) if isinstance(t, str) else parts.append(escape(str(t.value)))

    return ''.join(parts)
