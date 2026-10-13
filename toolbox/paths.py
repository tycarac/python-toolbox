import os
from pathlib import Path
import unicodedata

# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
WINDOWS_INVALID_FILENAME_CHARS = ['\\', '/', ':', '*', '|', '?', '>', '<', '"']
DASH_CHARS = ['\u2012', '\u2013', '\u2014', '\u2015', '\u2053']
REPLACE_CHARS = WINDOWS_INVALID_FILENAME_CHARS + DASH_CHARS


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
    return url.strip().strip('/') + '/' + '/'.join(map(lambda x: x.strip().strip('/'), paths))


# _____________________________________________________________________________
def sanitize_filename(filename: str):
    """Returns sanitized filename using ASCII character set
    :param filename: string without file path
    :return: sanitized filemane

    Leading/trailing/multiple whitespaces removed.
    Unicode dashes converted to ASCII dash but other unicode characters removed.
    No checks on None, leading/trailing dots, or filename length.
    """
    filename = ' '.join(filename.split())
    for ch in REPLACE_CHARS:
        if ch in filename:
            filename = filename.replace(ch, '-')
    if not filename.isascii():
        filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    if len(filename) < 1:
        raise ValueError('empty string')
    else:
        return filename