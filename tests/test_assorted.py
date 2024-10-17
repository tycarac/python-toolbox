import logging.config
from datetime import date, datetime
from typing import Union

import pytest

from toolbox.assorted import tax_year_from_date

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (date(2022,6,30), 'FY22'),
    (date(2022, 7, 1), 'FY23'),
    (date(2022, 12, 31), 'FY23'),
    (date(2023, 1, 1), 'FY23'),
    (date(2023, 6, 30), 'FY23'),
    (date(2023, 7, 1), 'FY24'),
    (date(2023, 12, 31), 'FY24'),
    (date(2024, 1, 1), 'FY24'),
    (date(2024, 6, 30), 'FY24'),
    (date(2024, 7, 1), 'FY25'),
])
def test_tax_year_from_date(given: Union[date, datetime], expected):
    assert tax_year_from_date(given) == expected
