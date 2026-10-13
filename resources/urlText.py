import certifi
import logging
from pathlib import Path
import time
from typing import Union
from urllib3 import exceptions, make_headers, Retry, PoolManager, Timeout

_logger = logging.getLogger(__name__)
_CACHE_AGE: int = 6 * 3600


# _____________________________________________________________________________
class UrlText:

    _url_headers = make_headers(keep_alive=False, accept_encoding=True)
    _url_headers |= {'Accept': 'text/*', 'Accept-Charset': 'utf-8', 'User-Agent': 'Mozilla/5.0'}
    _url_retries = Retry(total=4, backoff_factor=3, status_forcelist=[500, 502, 503, 504])
    _url_client = PoolManager(timeout=Timeout(total=15.0), retries=_url_retries, block=True,
                              headers=_url_headers, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    # _____________________________________________________________________________
    @staticmethod
    def __is_cached(local_path: Path, cache_age: int) -> bool:
        # Test local path cache age
        is_cached = False
        if cache_age > 0 and local_path.exists():
            is_cached = local_path.stat().st_mtime > (time.time() - cache_age)

        _logger.debug(f'Cache tag, is cached: "{local_path.name}", {str(is_cached)}')
        return is_cached

    # _____________________________________________________________________________
    @staticmethod
    def __write_cached_text(data: Union[str, bytes], local_path: Path) -> str:
        _logger.debug(f'cache write text "{local_path.name}"')
        data_text = None
        try:
            data_text = data.decode('utf-8') if isinstance(data, bytes) else data
            local_path.write_text(data_text)
        except (UnicodeError, OSError):
            path = local_path.with_suffix('.raw.txt')
            _logger.exception(f'Decode error: {path.name}')
            path.write_bytes(data)

        return data_text

    # _____________________________________________________________________________
    @staticmethod
    def get(url: str, filepath: Path, cache_age: int = _CACHE_AGE, fields: dict[str, str] = None) -> (str, bool):
        _logger.debug('get')

        if UrlText.__is_cached(filepath, cache_age):
            return filepath.read_text(), True

        data = None
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            rsp = UrlText._url_client.request('GET', url, fields=fields)
            if rsp.status == 200:
                data = UrlText.__write_cached_text(rsp.data, filepath)
            else:
                _logger.debug(f'Bad response status {rsp.status} for {url}')
        except (exceptions.HTTPError, exceptions.SSLError):
            _logger.exception(f'GET error: {url}')

        return data, False
