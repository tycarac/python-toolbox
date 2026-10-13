from collections import namedtuple
import os
import re
import string
from urllib import parse

from .fileTools import sanitize_filepath

# https://tools.ietf.org/html/rfc3986
_URN_GENERIC_DELIMITERS = ':/?#[]@'
_URN_AUTHORITY_DELIMITERS = '/?#'
_URL_STRIP_CHARS = string.whitespace + '/'
_SPACE_CHARS = '\u00A0\u2002\u2003'  # Does not include HTML specialized spaces

UrlParts = namedtuple('UrlParts', ['scheme', 'authority', 'path', 'query', 'fragment'])
UrlAuthorityParts = namedtuple('UrlAuthorityParts', ['user', 'host', 'port'])

re_url = re.compile(r'^(?:([a-z][a-z0-9+-.]*):(?://)?)??([^:/]+(?::\d{1,5})?)?' 
                    r'(?:(/[^?#]*))?(?:\?([^#]*))?(?:#(.*))?$', re.IGNORECASE)


# _____________________________________________________________________________
def url_join(url: str, /, *paths: str) -> str:
    """Returns URL by combining url with each of the arguments in turn
    :param url: base URL
    :param paths: paths to be added
    :return: URL

    Does not validate URL
    """
    u = url.strip(_URL_STRIP_CHARS)
    p = '/'.join(map(lambda x: x.strip(_URL_STRIP_CHARS), filter(lambda p: p, paths)))
    return f'{u}/{p}' if p and u else f'{u}{p}'


# _____________________________________________________________________________
def url_path_suffix(url: str) -> str:
    """
    The final component's last suffix, if any.  Includes leading period (eg: .'html').

    Parsing:
    1. Use urlparse to remove any trailing URL parameters.  Note a) "path" will contain the hostname when the URL
    does not start with '//' and b) "path" can be empty string but never None.
    2. Strip traling URL separator '/' and remove LHS far right URL separator
    """
    path = parse.urlparse(parse.unquote(url)).path.strip()
    if (j := path.rfind('.', path.rfind('/') + 1, len(path) - 1)) >= 0:
        return path[j:]
    return ''


# _____________________________________________________________________________
def url_to_pathname(url: str) -> str:
    """Returns MS-Windows sanitized filepath from a URL
    :param url: string
    :return: sanitized filename

    RFC 8089: The "file" URI Scheme
    """
    urlp = url_split(url)
    st = url_join(url_split_authority(urlp.authority).host, urlp.path) if urlp.authority else urlp.path
    path = ' '.join(parse.unquote_plus(st.strip(_URL_STRIP_CHARS)).split())
    if '/' != os.sep:
        path = path.replace('/', os.sep)
    pathname = sanitize_filepath(path)
    return pathname


# _____________________________________________________________________________
def url_split(url: str):
    """Parse a URL into five parts of: <scheme>://<authority>/<path>?<query>#<fragment>
    :param url: URL
    :return: tuple: (scheme, authority, path, query, fragment)
    """
    scheme, authority, path, query, fragment = '', '', '', None, None
    if match := re_url.match(url):
        if grp := match.group(1):
            scheme = grp
        if grp := match.group(2):
            authority = grp
        if grp := match.group(3):
            path = grp
        query = match.group(4)
        fragment = match.group(5)

    return UrlParts(scheme, authority, path, query, fragment)


# _____________________________________________________________________________
def url_split_authority(auth: str) -> (str, str, str):
    user, port = None, None
    if (loc_at := auth.find('@')) > 0:
        user = auth[:loc_at]
        auth = auth[loc_at + 1:]
    if (loc_colon := auth.find(':')) > 0:
        port = int(auth[loc_colon + 1:])
        auth = auth[:loc_colon]
    return UrlAuthorityParts(user, auth, port)

