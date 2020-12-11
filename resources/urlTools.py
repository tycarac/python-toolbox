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

re_url = re.compile(r'^(?:([a-zA-Z][a-zA-Z0-9+-.]*):(?://)?)??([^:/]+(?::\d{1,5})?)?'
                    r'(?:(/[^?#]*))?(?:\?([^#]*))?(?:#(.*))?$')


# _____________________________________________________________________________
def url_join(url: str, /, *paths: str) -> str:
    """Returns URL by combining url with each of the arguments in turn
    :param url: base URL
    :param paths: paths to be added
    :return: URL

    Does not validate URL.
    """
    if not (p := '/'.join(filter(lambda x: x, map(lambda x: x.strip(), paths)))):
        return url
    up = f'{u}/{p}' if (u := url.rstrip(_URL_STRIP_CHARS)) else p

    scheme, separator, remainder = up.partition('://')
    while '//' in remainder:
        remainder = remainder.replace('//', '/')
    if not separator:
        while '//' in scheme:
            scheme = scheme.replace('//', '/')

    return f'{scheme}{separator}{remainder}'


# _____________________________________________________________________________
def url_path_suffix(url: str) -> str:
    """
    The final component's last suffix, if any.  Includes leading period (eg: .'html').

    Parsing:
    1. Use urlparse to remove any trailing URL parameters.  Note a) "path" will contain the hostname
    when the URL does not start with '//' and b) "path" can be empty string but never None.
    2. Strip trailing URL separator '/' and remove LHS far right URL separator
    3. Ignore paths without '/' characters
    """
    path = parse.urlparse(parse.unquote(url)).path.strip()
    if (j := path.rfind('/')) >= 0 and (k := path.rfind('.', j + 1, len(path) - 1)) >= 0:
        return path[k:]
    return ''


# _____________________________________________________________________________
def url_to_pathname(url: str) -> str:
    """Returns MS-Windows sanitized filepath from a URL
    :param url: string
    :return: sanitized filename

    RFC 8089: The "file" URI scheme
    """
    urlp = url_split(parse.unquote(url))
    st = url_join(url_split_authority(urlp.authority).host, urlp.path) if urlp.authority else urlp.path
    path = ' '.join(parse.unquote_plus(st.strip(_URL_STRIP_CHARS)).split())
    if '/' != os.sep:
        path = path.replace('/', os.sep)
    return sanitize_filepath(path)


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
def url_split_authority(url: str) -> (str, str, str):
    """
    Returns the authority of a URL which is made of the userinfo, the hostname and the port.
    The userinfo and port are optional and a default port is assumed based on the scheme.
    """
    user, port = None, None
    auth = authority = url_split(url).authority
    if (loc_colon := authority.find(':')) > 0:
        port = int(authority[loc_colon + 1:])
        auth = auth[:loc_colon]
    if (loc_at := authority.find('@')) > 0:
        user = authority[:loc_at]
        auth = auth[loc_at + 1:]
    return UrlAuthorityParts(user, auth, port)
