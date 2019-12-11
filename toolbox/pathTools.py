import os
from pathlib import Path
import unicodedata
from urllib import parse

# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
WINDOWS_FOLDER_SEPARATOR_CHARS = ['\\', '/']
WINDOWS_INVALID_CHARS = [':', '*', '|', '?', '>', '<', '"']
WINDOWS_INVALID_FILENAME_CHARS = WINDOWS_INVALID_CHARS + WINDOWS_FOLDER_SEPARATOR_CHARS
DASH_CHARS = ['\u2012', '\u2013', '\u2014', '\u2015', '\u2053']
FILENAME_REPLACE_CHARS = WINDOWS_INVALID_FILENAME_CHARS + DASH_CHARS
PATHNAME_REPLACE_CHARS = WINDOWS_INVALID_CHARS + DASH_CHARS


# _____________________________________________________________________________
def is_parent(parent: Path, path: Path):
    """Returns True is path has the same parent path as parent
    :param parent:
    :param path:
    :return: True if parent path is contained in path
    """
    parent = parent.resolve()
    path = path.resolve()
    return str(path).startswith(str(parent))


# _____________________________________________________________________________
def __delete_empty_directories(folder):
    """Deletes all empty child folders under a parent folder
    :param folder: parent folder
    :return: List of deleted folders
    """
    deleted_folders = []
    for root, dirs, _ in os.walk(folder, topdown=False):
        for dir in dirs:
            name = os.path.join(root, dir)
            if not len(os.listdir(name)):
                deleted_folders.append(dir)
                os.rmdir(name)

    return deleted_folders


# _____________________________________________________________________________
def join_url_path(url, *paths):
    """Returns URL by combining url with each of the arguments in turn
    :param url: base URL
    :param paths: paths to be added
    :return: URL

    Does not validate URL
    """
    return '%s/%s/' % (url.strip().strip('/'), '/'.join(map(lambda x: x.strip().strip('/'), paths)))


# _____________________________________________________________________________
def sanitize_filename(filename: str):
    """Returns MS-Windows sanitized filename using ASCII character set
    :param filename: string
    :return: sanitized filename

    Leading/trailing/multiple whitespaces removed.
    Unicode dashes converted to ASCII dash but other unicode characters removed.
    No checks on None, leading/trailing dots, or filename length.
    """
    filename = ' '.join(parse.unquote(filename).split())
    for ch in FILENAME_REPLACE_CHARS:
        if ch in filename:
            filename = filename.replace(ch, '-')
    if not filename.isascii():
        filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    if len(filename) < 1:
        raise ValueError('empty string')

    return filename


# _____________________________________________________________________________
def urlpath_to_pathname(url: str):
    """Returns MS-Windows sanitized filepath from a URL
    :param url: string
    :return: sanitized filename

    RFC 8089: The "file" URI Scheme
    """
    pathname = ' '.join(parse.unquote(url).strip().split())
    pathname = '\\'.join(pathname.strip('/').split('/'))
    for ch in PATHNAME_REPLACE_CHARS:
        if ch in pathname:
            pathname = pathname.replace(ch, '-')
    if not pathname.isascii():
        pathname = unicodedata.normalize('NFKD', pathname).encode('ASCII', 'ignore').decode('ASCII')
    if len(pathname) < 1:
        raise ValueError('empty string')

    return pathname
