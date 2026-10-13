import io
import os
import string
import unicodedata
import zipfile
from pathlib import Path
from typing import Tuple, LiteralString, Any, AnyStr
from urllib import parse

# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
_FOLDER_SEPARATOR_CHARS = ['\\', '/']
_DASH_CHARS = ['\u2012', '\u2013', '\u2014', '\u2015', '\u2053']
_WINDOWS_INVALID_CHARS = [':', '*', '|', '?', '>', '<', '"']
_WINDOWS_INVALID_FILENAME_CHARS = _WINDOWS_INVALID_CHARS + _FOLDER_SEPARATOR_CHARS
_FILENAME_REPLACE_CHARS = _WINDOWS_INVALID_FILENAME_CHARS + _DASH_CHARS
_PATHNAME_REPLACE_CHARS = _WINDOWS_INVALID_CHARS + _DASH_CHARS
_URL_STRIP_CHARS = string.whitespace + '/'
_SPACE_CHARS = ['\u00A0', '\u2002', '\u2003']  # Does not include HTML specialized spaces


# _____________________________________________________________________________
def is_parent(parent: Path, path: Path) -> bool:
    """Returns True is path has the same parent path as parent
    :param parent:
    :param path:
    :return: True if parent path is contained in path
    """
    return str(path.resolve()).startswith(str(parent.resolve()))


# _____________________________________________________________________________
def delete_empty_directories(directory: os.PathLike) -> list[LiteralString]:
    """Deletes all empty child folders under 'directory'
    :param directory: parent folder
    :return: List of deleted folders
    """
    deleted_folders: list[LiteralString] = []
    for root, folders, _ in os.walk(directory, topdown=False):
        for folder in folders:
            loc: LiteralString = os.path.join(root, folder)
            with os.scandir(loc) as it:
                if next(it, None) is None:
                    deleted_folders.append(loc)
                    os.rmdir(loc)

    return deleted_folders


# _____________________________________________________________________________
def sanitize_filename(filename: str, remove_dot=False) -> str:
    """Returns MS-Windows sanitized filename using ASCII character set
    :param filename: string
    :param remove_dot: bool
    :return: sanitized filename

    Remove URL character encodings and leading/trailing/multiple whitespaces.
    Convert Unicode dashes to ASCII dash but other unicode characters removed.
    Optionally, remove doc character but not from leading
    No checks on None, leading/trailing dots, or filename length.
    """
    fname: str = ' '.join(parse.unquote(filename).split())
    for ch in _FILENAME_REPLACE_CHARS:
        if ch in fname:
            fname = fname.replace(ch, '-')
    if not fname.isascii():
        fname = unicodedata.normalize('NFKD', fname).encode('ASCII', 'ignore').decode('ASCII')
    if remove_dot and fname.find('.', 1) > 0:
        fname = fname[0] + fname[1:].replace('.', '')

    return fname


# _____________________________________________________________________________
def join_urlpath(url, *paths: str) -> str:
    """Returns URL by combining url with each of the arguments in turn
    :param url: base URL
    :param paths: paths to be added
    :return: URL

    Does not validate URL
    """
    u: str = url.strip(_URL_STRIP_CHARS)
    p: str = '/'.join(map(lambda x: x.strip(_URL_STRIP_CHARS), paths))
    return f'{u}/{p}' if p else u


# _____________________________________________________________________________
def urlpath_to_pathname(url: str):
    """Returns MS-Windows sanitized filepath from a URL
    :param url: string
    :return: sanitized filename

    RFC 8089: The "file" URI Scheme
    """
    urlp = parse.urlparse(' '.join(parse.unquote(url).strip().split()))
    path = urlp.path.strip(_URL_STRIP_CHARS).replace('/', '\\')

    if not urlp.hostname:
        pathname = path
    else:
        pathname = f'{urlp.hostname}\\{path}' if path else urlp.hostname

    for ch in _PATHNAME_REPLACE_CHARS:
        if ch in pathname:
            pathname = pathname.replace(ch, '-')
    if not pathname.isascii():
        pathname = unicodedata.normalize('NFKD', pathname).encode('ASCII', 'ignore').decode('ASCII')

    return pathname


# _____________________________________________________________________________
def url_suffix(url: str) -> str:
    """
    The final component's last suffix, if any.  Includes leading period (eg: .'html').

    Parsing:
    1. Use urlparse to remove any trailing URL parameters.  Note a) "path" will contain the hostname when the URL
    does not start with '//' and b) "path" can be empty string but never None.
    2. Strip traling URL separator '/' and remove LHS far right URL separator
    """
    path: LiteralString = parse.urlparse(parse.unquote(url)).path.strip()
    if (j := path.rfind('.', path.rfind('/') + 1, len(path) - 1)) >= 0:
        return path[j:]
    return ''


# _____________________________________________________________________________
def open_files(path: os.PathLike) -> Tuple[str, int]:
    """Iterate over a root path returning an open file handle for each file found - including file in archives
    :return: Tuple[filename:str,file handle:int]
    """
    for root, _, filenames in os.walk(str(path)):
        # Iterate over files found in directory
        for filename in filenames:
            path = Path(root, filename).resolve()
            rel_path_str = str(Path(path.relative_to(path), path.name))

            # Test if file is an archive
            if file_suffix(filename) in ['.zip', '.gzip', '.gz']:
                with zipfile.ZipFile(io.BytesIO(path.read_bytes())) as zp:
                    # Iterate over files inside archive
                    for zipinfo in filter(lambda z: not z.is_dir(), zp.infolist()):
                        with zp.open(zipinfo) as file_handle:
                            yield f'{rel_path_str}|{zipinfo.filename}', file_handle
            else:
                # Yield non-archive file
                with open(path) as file_handle:
                    yield rel_path_str, file_handle


# _____________________________________________________________________________
def file_suffix(fp: str) -> str:
    """Extract the file suffix from a path

    :param fp:
    :return:
    """
    loc: int = max(fp.rfind('\\'), fp.rfind('/')) + 1
    if (pos := fp.rfind('.', loc)) > 0 and fp[loc] != '.':
        return fp[pos:]
    return ''
