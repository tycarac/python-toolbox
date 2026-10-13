from pathlib import Path
from resources.urlText import UrlText
import logging
from os import PathLike
from typing import Union

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def get(url: str, /, *filename: Union[str, PathLike]):
    filepath = Path(*filename).resolve()
    data, is_cached = UrlText.get(url, filepath)
    return data, is_cached


# _____________________________________________________________________________
def test_get_text(tmpdir):
    _logger.debug('test_get_text')
    testdir = str(tmpdir)
    _logger.debug(f'Using tmp dir: {testdir}')

    data, is_cached = get('https://www.npr.org/proxy/listening/v2/newscast/1/recommendations',
                          testdir, 'recommendations.txt')
    assert(data is not None and len(data) > 0)
    assert(is_cached is False)

    data, is_cached = get('https://www.npr.org/proxy/listening/v2/newscast/1/recommendations',
                          testdir, 'recommendations.txt')
    assert(data is not None and len(data) > 0)
    assert(is_cached is True)
