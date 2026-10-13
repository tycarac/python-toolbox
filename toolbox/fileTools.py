from datetime import timedelta, date, datetime, time
import os
from pathlib import Path
import string
from typing import List, Tuple
import unicodedata
from urllib import parse
import zipfile

# Filename constants
# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
_FOLDER_SEPARATOR_CHARS = '\\/'
_DASH_CHARS = '\u2012\u2013\u2014\u2015\u2053'
_WINDOWS_INVALID_CHARS = ':*|?><"'
_WINDOWS_INVALID_FILENAME_CHARS = _WINDOWS_INVALID_CHARS + _FOLDER_SEPARATOR_CHARS
_FILENAME_REPLACE_CHARS = _WINDOWS_INVALID_CHARS + _DASH_CHARS
_PATHNAME_REPLACE_CHARS = _FILENAME_REPLACE_CHARS + _FOLDER_SEPARATOR_CHARS


# _____________________________________________________________________________
def file_suffix(fp: str) -> str:
    """Extract the file suffix from a pathname
    Extension is the last dot to the end, ignoring leading dot.
    :param fp:
    :return: file suffix or empty string
    """
    loc = max(fp.rfind('\\'), fp.rfind('/')) + 1  # Find to avoid matching dot in path parent
    if (pos := fp.rfind('.', loc)) > 0 and fp[loc] != '.':
        return fp[pos:]
    return ''


# _____________________________________________________________________________
def is_parent(parent: str, path: str, /) -> bool:
    """Returns True is path has the same parent path as parent
    :param parent: string
    :param path: string
    :return: True if parent path is contained in path
    """
    return os.path.normpath(path).startswith(os.path.normpath(parent))


# _____________________________________________________________________________
def sanitize_filepath(filename: str, /, replace_dot=False, replace_folder_sep=False) -> str:
    """Returns MS-Windows sanitized filepath using ASCII character set
    :param filename: string
    :param replace_dot: bool
    :param replace_folder_sep: bool
    :return: sanitized filepath

    Remove URL character encodings and leading/trailing whitespaces.
    Replace whitespaces with '-' character (for Linux ease-of-use)
    Convert Unicode dashes to ASCII dash, but other unicode characters removed.
    Optionally, remove dot character but not from leading
    No checks on None, for leading/trailing dots, or filename length.
    """
    join_ch = ' ' if os.name == 'nt' else '-'
    fname = join_ch.join(parse.unquote(filename).split())

    # Replace invalid characters with '-' and replace unicode dashes with ASCII '-'
    for ch in _FILENAME_REPLACE_CHARS:
        if ch in fname:
            fname = fname.replace(ch, '-')
    # Replace folder separators as instructed
    for ch in _FOLDER_SEPARATOR_CHARS:
        if (replace_folder_sep or ch != os.sep) and ch in fname:
            fname = fname.replace(ch, '-')
    if not fname.isascii():
        fname = unicodedata.normalize('NFKD', fname).encode('ASCII', 'ignore').decode('ASCII')
    if replace_dot and fname.find('.', 1) > 0:
        fname = fname[0] + fname[1:].replace('.', '-')

    return fname


# =============================================================================
# File operations
# _____________________________________________________________________________
def delete_empty_directories(path: os.PathLike) -> List[str]:
    """Deletes all empty child folders under a parent folder
    :param path:
    :return: List of deleted folders
    """
    deleted_folders = []
    for parent, dirs, _ in os.walk(path, topdown=False):
        for dir in [os.path.join(parent, d) for d in dirs]:
            with os.scandir(dir) as it:
                if next(it, None) is None:
                    try:
                        os.rmdir(dir)
                        deleted_folders.append(dir)
                    except PermissionError:
                        pass

    return deleted_folders


# _____________________________________________________________________________
def delete_empty_old_files(path: os.PathLike, age: timedelta = None, /) -> (List[str], List[str]):
    """Deletes all empty child folders under a parent folder
    Notes:
     - times are UTC
    :param path: parent folder
    :param age:
    :param include_empty:
    :return: Tuple of deleted files, deleted folders and errors
    """
    cutoff = None
    if age:
        if age.days > 0:
            cutoff = (datetime.now() - age).replace(hour=0, minute=0, second=0).timestamp()
        else:
            cutoff = (datetime.now() - age).timestamp()

    deleted_folders, deleted_files, errors = [], [], []
    for parent, dirs, files in os.walk(path, topdown=False):
        # Delete empty and old files
        for file in [os.path.join(parent, f) for f in files]:
            if (cutoff and os.path.getmtime(file) < cutoff) or os.path.getsize(file) == 0:
                try:
                    os.remove(file)
                    deleted_files.append(file)
                except PermissionError:
                    errors.append(file)

        # Delete empty directories
        for dir in [os.path.join(parent, d) for d in dirs]:
            with os.scandir(dir) as it:
                if next(it, None) is None:
                    try:
                        os.rmdir(dir)
                        deleted_folders.append(dir)
                    except PermissionError:
                        errors.append(dir)

    return deleted_files, deleted_folders, errors


# _____________________________________________________________________________
def open_files(path: os.PathLike) -> Tuple[str, int]:
    """Iterate over a root path returning an open file handle for each file found - including file in archives
    :return: Tuple[filename:str,file handle:int]
    """
    for root, _, filenames in os.walk(path):
        # Iterate over files found in directory
        rel_root_path = os.path.relpath(root, path)
        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_file_path = os.path.join(rel_root_path, filename)[2:]
            # Test if file is an archive
            if file_suffix(filename) in ['.zip', '.gzip', '.gz']:
                with zipfile.ZipFile(file_path) as zh:
                    # Iterate over files inside archive
                    for zipinfo in filter(lambda z: not z.is_dir(), zh.infolist()):
                        with zh.open(zipinfo) as file_handle:
                            yield f'{rel_file_path}|{zipinfo.filename}', file_handle
            else:
                # Yield non-archive file
                with open(file_path) as fh:
                    yield rel_file_path, fh
