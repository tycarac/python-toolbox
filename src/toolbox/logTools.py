"""

Notes:
- The logging Formatter formats an exception as a string and caches it.  The first Logging handler does the exception
formating and caching.  Subsequent calls to logging handlers use the same cached exception text.  The cached exception
string is stored in LogRecord record.exec_text and must be cleared if a different exception format is required.  Thus,
custom logging formatters should be added after standard Logging formatters.
"""
import logging
import logging.config
from datetime import datetime, UTC
from pathlib import Path
from sys import stdout
from typing import Any

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
class NoExceptionFormatter(logging.Formatter):
    """Remove exception details from logger formatter so to declutter log downloads
    """

    def format(self, record: logging.LogRecord) -> str:
        record.exc_text = ''
        return super().format(record)

    def formatException(self, ei) -> str:
        return ''


# _____________________________________________________________________________
class MessageFormatter(logging.Formatter):
    """Remove all exception details from logger formatter except for message so to declutter log downloads
    """

    def format(self, record: logging.LogRecord) -> str:
        record.exc_text = ''
        return super().format(record)

    def formatException(self, ei) -> str:
        lei = (ei[0], ei[1], None)
        return repr(super().formatException(lei))


# _____________________________________________________________________________
class OneLineFormatter(logging.Formatter):
    """Covert exception details to single line to simplify log downloads processing
    """

    def format(self, record: logging.LogRecord) -> str:
        if text := super().format(record):
            text = text.strip().replace('\n', '|')
        return text


# _____________________________________________________________________________
class PathFileHandler(logging.FileHandler):
    """Extends FileHandler to create the directory, if required, for the log file.

    Note this has some security risk as the file path is arbitrary and could be any location.
    """

    def __init__(self, filename, mode='a', encoding=None):
        Path.mkdir(Path(filename).parent, parents=True, exist_ok=True)
        super().__init__(filename, mode, encoding)


# _____________________________________________________________________________
def initialize_logger(lconfig: dict[str, Any], start_dt: datetime) -> None:
    if not lconfig:
        return

    logging.config.dictConfig(lconfig)
    logging.captureWarnings(True)

    start_dt_utc = start_dt.astimezone(UTC)
    _logger.info(f'Now: {start_dt.strftime("%a  %d-%b-%y  %I:%M:%S %p")}')
    _logger.info(f'UTC: {start_dt_utc.strftime("%a  %d-%b-%y  %I:%M:%S %p")}')


# _____________________________________________________________________________
def initialize_logger_coded(app_base_folder: Path, log_base_name: str) -> None:
    logging.captureWarnings(True)
    log_folder = Path(app_base_folder, 'logs').resolve()
    Path.mkdir(log_folder, parents=True, exist_ok=True)

    # --- Formatters ---
    brief_formatter = logging.Formatter("%(levelname)-6s %(msg)s")
    context_formatter = logging.Formatter("%(levelname)-6s %(name)-12s %(message)s")
    no_exception_formatter = NoExceptionFormatter()
    message_formatter = MessageFormatter()

    # --- Handlers ---
    output_file_handler = logging.FileHandler(mode='wt', encoding='utf-8',
                                              filename=Path(log_folder, f'{log_base_name}.output.log'))
    output_file_handler.setLevel(logging.INFO)
    output_file_handler.setFormatter(no_exception_formatter)

    debug_file_handler = logging.FileHandler(mode='wt', encoding='utf-8',
                                             filename=Path(log_folder, f'{log_base_name}.debug.log'))
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(context_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(no_exception_formatter)
    console_handler.setStream(stdout)

    # --- Root Logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(output_file_handler)
    root_logger.addHandler(console_handler)
