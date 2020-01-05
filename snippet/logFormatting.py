import json
import logging, logging.config
from pathlib import Path
from sys import exc_info
from string import whitespace

from toolbox import logTools


# _____________________________________________________________________________
# Setup
output_filepath = Path('log.output.log')
debug_filepath = Path('log.debug.log')
if output_filepath.exists():
    output_filepath.unlink()
if debug_filepath.exists():
    debug_filepath.unlink()

# Common variables
logger = logging.getLogger(__name__)
use_config_file = True

if use_config_file:
    logging.captureWarnings(True)
    with Path('log.config.json') as p:
        logging.config.dictConfig(json.loads(p.read_text()))
else:
    logger.setLevel(logging.DEBUG)

    format_brief = logging.Formatter('%(message)s')
    format_normal = logging.Formatter('%(levelname)-6s %(name)-20s %(message)s')
    format_msg = logTools.MessageFormatter(fmt='%(levelname)-6s %(message)s')

    handler_output_logfile = logging.FileHandler(output_filepath)
    handler_output_logfile.setLevel(logging.INFO)
    handler_output_logfile.setFormatter(format_brief)

    handler_debug_logfile = logging.FileHandler(debug_filepath)
    handler_debug_logfile.setLevel(logging.DEBUG)
    handler_debug_logfile.setFormatter(format_normal)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)
    handler_console.setFormatter(format_msg)

    logger.addHandler(handler_output_logfile)
    logger.addHandler(handler_debug_logfile)
    logger.addHandler(handler_console)


try:
    logger.debug('log debug')
    logger.info('log info')
    try:
        raise ValueError('bad value')
    except Exception as exc:
        logger.exception('log exception')
    logger.info('end of tests')
except Exception as exc:
    logger.exception('Unexpected')
finally:
    logger.info('done')
