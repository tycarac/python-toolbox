from datetime import date, datetime
from typing import Union


# _____________________________________________________________________________
def str_to_bool(s: Union[str, bool]) -> bool:
    return s if type(s) is bool else s.lower() in ('true', 't', 'yes', '1')


# _____________________________________________________________________________
def is_blank(s: str) -> bool:
    return not (s and s.strip())


# _____________________________________________________________________________
def is_not_blank(s: str) -> bool:
    return bool(s and s.strip())


# _____________________________________________________________________________
def normalize_blank(s: str) -> str:
    return s.strip() if s else ''


# _____________________________________________________________________________
def tax_year_from_date(d: Union[date, datetime]) -> str:
    return f'FY{(d.year if (d.month <= 6) else d.year + 1) % 100}'


# _____________________________________________________________________________
def multisort(coll: list, specs):
    for key, itr in reversed(specs):
        coll.sort(key=key, reverse=itr)
    return coll
