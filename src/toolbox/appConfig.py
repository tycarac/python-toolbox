import logging.handlers
import platform
import tomllib
from pathlib import Path
from string import Template
from typing import Any

from platformdirs import PlatformDirs

# Common variables
_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def load_config_toml(file_path: Path) -> dict[str, Any]:
    try:
        # Opening file as binary needed to detect character encoding
        with file_path.open('rb') as f:
            return tomllib.load(f)
    except FileNotFoundError as ex:
        _logger.exception(f'Config file "{file_path}" not found')
        raise ex
    except tomllib.TOMLDecodeError as ex:
        _logger.exception(f'Config file "{file_path}" TOML decoding error')
        raise ex
    except PermissionError as ex:
        _logger.exception(f'Config file "{file_path}" permission denied')
        raise ex


# _____________________________________________________________________________
class AppConfig:
    _os_type: str
    _app_name: str
    _app_author: str
    _workspace_name: str
    _workspace_dir: Path
    _config_dir: Path
    _input_dir: Path
    _output_dir: Path
    _data_dir: Path
    _cache_dir: Path
    _log_dir: Path

    _config: dict = {}
    _match_equal_quantities_first: bool
    _enable_quack_protocol: bool

    # _____________________________________________________________________________
    def __init__(self, workspace_dir: Path, app_name: str, app_author: str = "tycarac"):
        _logger.debug(f'__init__ app_name "{app_name}"')

        self._workspace_dir = workspace_dir
        self._workspace_name = workspace_dir.stem
        self._app_name = app_name
        self._app_author = app_author
        self._os_type = platform.system()  # 'Windows', 'Darwin' (macOS), or 'Linux'
        dirs: PlatformDirs = PlatformDirs(self._workspace_name, self._app_author, opinion=True)

        # Config (use project config first if it exists)
        self._config_dir: Path = dirs.user_config_path if dirs.user_config_path.exists() else Path(workspace_dir,
                                                                                                   'config').resolve()
        for path in (self._config_dir, Path(self._workspace_dir, 'config')):
            cpath: Path = Path(path, 'app.config.toml').resolve()
            if cpath.exists():
                _logger.debug(f'Load config file: "{cpath}"')
                self._config.update(load_config_toml(cpath))
                self.update_from_entries()

        # Best practice locations: Data, Cache, Logs
        self._data_dir: Path = dirs.user_data_path  # Databases, persistent state
        self._cache_dir: Path = dirs.user_cache_path  # Temporary query caches
        self._log_dir: Path = dirs.user_log_path  # App logs
        for dir in [self._data_dir, self._cache_dir, self._log_dir]:
            dir.mkdir(parents=True, exist_ok=True)

        # Other app locations: Input, Output
        self._input_dir = Path(workspace_dir, 'input').resolve()
        self._output_dir = Path(workspace_dir, 'output').resolve()
        for dir in [self._input_dir, self._output_dir]:
            dir.mkdir(parents=True, exist_ok=True)

    # _____________________________________________________________________________
    def update_from_entries(self) -> None:
        # Set defaults for config entries
        _match_equal_quantities_first = False
        _enable_quack_protocol = False

        # Check for config [processing]
        if p := self._config.get('processing'):
            if 'match-equal-quantities-first' in p:
                self._match_equal_quantities_first = p['match-equal-quantities-first']

        # Check for config [processing]
        if d := self._config.get('duckdb'):
            if 'enable-quack-protocol' in d:
                self._enable_quack_protocol = d['enable-quack-protocol']

    # _____________________________________________________________________________
    @property
    def input_dir(self) -> Path:
        return self._input_dir

    # _____________________________________________________________________________
    @property
    def output_dir(self) -> Path:
        return self._output_dir

    # _____________________________________________________________________________
    @property
    def data_dir(self) -> Path:
        return self._data_dir

    # _____________________________________________________________________________
    @property
    def config_dir(self) -> Path:
        return self._config_dir

    # _____________________________________________________________________________
    @property
    def log_dir(self) -> Path:
        return self._log_dir

    # _____________________________________________________________________________
    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    # _____________________________________________________________________________
    @property
    def config(self) -> dict:
        return self._config

    # _____________________________________________________________________________
    def update(self, d: dict) -> None:
        self._config.update(d)

    # _____________________________________________________________________________
    @property
    def match_equal_quantities_first(self) -> bool:
        return self._match_equal_quantities_first

    # _____________________________________________________________________________
    @property
    def enable_quack_protocol(self) -> bool:
        return self._enable_quack_protocol

    # _____________________________________________________________________________
    def load_logging_config(self) -> dict[str, Any]:
        config_file_path: Path = Path(self._workspace_dir, 'config', 'app.logging.toml').resolve()
        if not config_file_path.exists():
            config_file_path = Path(self._config_dir, 'app.logging.toml').resolve()

        lconfig = {}
        if config_file_path.exists():
            sconfig = config_file_path.read_text()
            log_path_posix = self._log_dir.as_posix()
            tconfig = Template(sconfig).safe_substitute(logpath=log_path_posix, appname=self._app_name)
            lconfig = tomllib.loads(tconfig)

        return lconfig
