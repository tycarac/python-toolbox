import json
import logging.config
from pathlib import Path
import urllib3

TIME_JITTER_S = 10
URL_TIMEOUT_S = 20

logger = logging.getLogger(__name__)
url_headers = urllib3.make_headers(keep_alive=True, accept_encoding=True, disable_cache=True)
url_retries = urllib3.Retry(total=4, backoff_factor=5, status_forcelist=[500, 502, 503, 504])
url_client = urllib3.PoolManager(timeout=urllib3.Timeout(total=20.0), retries=url_retries, maxsize=10, block=True)


# _____________________________________________________________________________
def fetch_api_credentials(api_client):
    with Path(Path.home(), '.thystra', 'shared.api.json').open(mode='rt') as f:
        api_settings = json.load(f)

    try:
        client = api_settings['clients'][api_client]
        return client['scope'], client['client_id'], client['client_secret'], api_settings['oauth_url']
    except Exception as ex:
        logger.fatal(f'Failed configuration for API client: {api_client}')
        raise ex


# _____________________________________________________________________________
def get_oauth_token(api_client):
    try:
        logger.info(f'Fetching OAuth: {api_client}')
        scope, client_id, client_secret, oauth_url = fetch_api_credentials(api_client)
    except Exception as ex:
        logger.exception(f'Error fetching OAuth client config: {api_client}')
        return None

    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        payload = {
            'grant_type': 'client_credentials',
            'scope': scope,
            'client_id': client_id,
            'client_secret': client_secret
        }

        logger.debug(f'URL: {oauth_url}')
        headers.update(url_headers)
        rsp = url_client.request_encode_body('POST', oauth_url, headers=headers, fields=payload, encode_multipart=False)
        logger.debug(f'code: {rsp.status}')
        if rsp.status == 200:
            data = rsp.data
            result = json.loads(data.decode('utf-8'))
            return result["access_token"]
    except urllib3.exceptions.HTTPError as ex:
        logger.exception('HTTPError')
    except Exception as ex:
        logger.exception('generic exception')

    return None
