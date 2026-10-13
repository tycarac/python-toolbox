import logging.config
from collections.abc import Iterator
from contextlib import closing
from datetime import date, datetime
from decimal import Decimal
from sqlite3 import Connection, connect
from string.templatelib import Template

import pytest

from toolbox.assorted import date_to_tax_year, tsql

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize(
    'given, expected',
    [
        (date(2022, 6, 30), 'FY22'),
        (date(2022, 7, 1), 'FY23'),
        (date(2022, 12, 31), 'FY23'),
        (date(2023, 1, 1), 'FY23'),
        (date(2023, 6, 30), 'FY23'),
        (date(2023, 7, 1), 'FY24'),
        (date(2023, 12, 31), 'FY24'),
        (date(2024, 1, 1), 'FY24'),
        (date(2024, 6, 30), 'FY24'),
        (date(2024, 7, 1), 'FY25'),
    ],
)
def test_tax_year_from_date(given: date | datetime, expected: str) -> None:
    assert date_to_tax_year(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize(
    'template, expected_sql',
    [
        pytest.param(t'', '', id='empty'),
        pytest.param(t'SELECT 1', 'SELECT 1', id='static-sql'),
        pytest.param(
            t"SELECT '?' AS marker, '{{name}}' AS text\n", "SELECT '?' AS marker, '{name}' AS text\n", id='literal-text'
        ),
    ],
)
def test_tsql_without_parameters(template: Template, expected_sql: str) -> None:
    assert tsql(template) == (expected_sql, [])


# _____________________________________________________________________________
@pytest.mark.parametrize(
    'value',
    [
        pytest.param(None, id='null'),
        pytest.param(True, id='true'),
        pytest.param(False, id='false'),
        pytest.param(0, id='zero'),
        pytest.param(42, id='integer'),
        pytest.param(-7, id='negative-integer'),
        pytest.param(1.25, id='float'),
        pytest.param(Decimal('12.30'), id='decimal'),
        pytest.param(date(2026, 10, 13), id='date'),
        pytest.param(datetime(2026, 10, 13, 12, 34, 56), id='datetime'),
        pytest.param(b'\x00\xff', id='bytes'),
        pytest.param('', id='empty-string'),
        pytest.param("O'Reilly", id='quoted-string'),
        pytest.param('서울 café', id='unicode'),
    ],
)
def test_tsql_preserves_parameter_value_and_type(value: object) -> None:
    sql: str
    params: list[object]
    sql, params = tsql(t'SELECT {value}')

    assert sql == 'SELECT ?'
    assert params == [value]
    assert params[0] is value


# _____________________________________________________________________________
@pytest.mark.parametrize(
    'template, expected_sql, expected_params',
    [
        pytest.param(t'{1}', '?', [1], id='parameter-only'),
        pytest.param(t'{1} + {2}', '? + ?', [1, 2], id='boundary-parameters'),
        pytest.param(t'{1}{2}', '??', [1, 2], id='adjacent-parameters'),
        pytest.param(t'SELECT {2}, {1}, {2}', 'SELECT ?, ?, ?', [2, 1, 2], id='ordered-and-repeated'),
        pytest.param(t'SELECT {1}, {False}, {None}', 'SELECT ?, ?, ?', [1, False, None], id='mixed-types'),
        pytest.param(t'SELECT {1}' + t' + {2}', 'SELECT ? + ?', [1, 2], id='concatenated-templates'),
    ],
)
def test_tsql_parameter_positions(template: Template, expected_sql: str, expected_params: list[object]) -> None:
    assert tsql(template) == (expected_sql, expected_params)


# _____________________________________________________________________________
def test_tsql_preserves_literal_sql_around_parameters() -> None:
    value: str = 'Ada'
    template: Template = t"SELECT '?' AS marker, '{{name}}' AS text\nWHERE name = {value}\n"

    assert tsql(template) == ("SELECT '?' AS marker, '{name}' AS text\nWHERE name = ?\n", [value])


# _____________________________________________________________________________
def test_tsql_ignores_conversion_and_format_specifiers() -> None:
    value: Decimal = Decimal('12.345')
    sql: str
    params: list[object]
    sql, params = tsql(t'SELECT {value!s}, {value!r}, {value!a}, {value:.2f}')

    assert sql == 'SELECT ?, ?, ?, ?'
    assert params == [value] * 4
    assert all(param is value for param in params)


# _____________________________________________________________________________
@pytest.fixture
def sqlite_connection() -> Iterator[Connection]:
    connection: Connection
    with closing(connect(':memory:')) as connection:
        yield connection


# _____________________________________________________________________________
@pytest.mark.parametrize(
    'value',
    [
        pytest.param("O'Reilly", id='apostrophe'),
        pytest.param("' OR 1=1 --", id='sql-comment'),
        pytest.param("'; DROP TABLE users; --", id='sql-statement'),
    ],
)
def test_tsql_binds_sql_looking_strings_as_values(sqlite_connection: Connection, value: str) -> None:
    sql: str
    params: list[object]
    sql, params = tsql(t'SELECT {value}')

    assert sql == 'SELECT ?'
    assert params == [value]
    assert sqlite_connection.execute(sql, params).fetchone() == (value,)
    assert sqlite_connection.execute(*tsql(t"SELECT 'Ada' WHERE 'Ada' = {value}")).fetchall() == []
