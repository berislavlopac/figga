import os
from pathlib import Path
from inspect import isclass
from configparser import ConfigParser, DEFAULTSECT
from typing import ItemsView, Union


class Configuration:

    def __init__(self, config: dict, default=None):
        self._config = {key.lower(): value for key, value in config.items()}
        self._default = default

    def __getattr__(self, item: str):
        return self.get(item)

    def get(self, item: str, default='UNLIKELY default VALUE'):
        if default == 'UNLIKELY default VALUE':
            default = self._default
        value = self._config.get(item.lower(), default)
        if isclass(value) and issubclass(value, BaseException):
            raise value(f"{item} is not defined")
        if callable(value):
            return value(item)
        return value

    def items(self) -> ItemsView:
        return self._config.items()

    @classmethod
    def from_environ(cls, prefix: str, remove_prefix: bool=False, default=None) -> 'Configuration':
        prefix_length = len(prefix)
        config = {
            key[prefix_length:] if remove_prefix else key: value
            for key, value in os.environ.items() if key.startswith(prefix)
        }
        return cls(config, default=default)

    @classmethod
    def from_files(cls, *files: Union[str, os.PathLike], section: str=DEFAULTSECT, default=None) -> 'Configuration':
        config = ConfigParser(default_section=section)
        for file_path in files:
            file_path = Path(file_path)
            if not file_path.is_absolute():
                file_path = Path.cwd() / file_path
            if file_path.exists():
                config.read(file_path)
        config = {
            key: value for key, value in config[section].items()
        }
        return cls(config, default=default)
