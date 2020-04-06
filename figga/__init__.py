import os
from configparser import ConfigParser, DEFAULTSECT
from inspect import isclass
from pathlib import Path
from typing import ItemsView, Union


class Configuration:
    def __init__(self, config: dict, default=None):
        self._config = {key.lower(): value for key, value in config.items()}
        self._default = default

    def __getattr__(self, item: str):
        return self.get(item)

    def get(self, item: str, **kwargs):
        """ Retrieves a single configuration value.
        """
        default = kwargs.get("default", self._default)
        value = self._config.get(item.lower(), default)
        if isclass(value) and issubclass(value, BaseException):
            raise value(f"{item} is not defined")
        if callable(value):
            return value(item)
        return value

    def items(self) -> ItemsView:
        """ Returns a dict containing all configuration values.
        """
        return self._config.items()

    @classmethod
    def from_environ(
        cls, prefix: str, remove_prefix: bool = False, default=None
    ) -> "Configuration":
        """ Constructs a Configuration instance from a set of environment
            variables sharing the same prefix. Optionally, the prefix can
            be removed from the configuration values.
        """
        prefix_length = len(prefix)
        config = {
            key[prefix_length:] if remove_prefix else key: value
            for key, value in os.environ.items()
            if key.startswith(prefix)
        }
        return cls(config, default=default)

    @classmethod
    def from_files(
        cls, *files: Union[str, os.PathLike], section: str = DEFAULTSECT, default=None
    ) -> "Configuration":
        """ Constructs a Configuration instance from one or more INI files.
        """
        config = ConfigParser(default_section=section)
        for file_path in files:
            file_path = Path(file_path)
            if not file_path.is_absolute():
                file_path = Path.cwd() / file_path
            if file_path.exists():
                config.read(file_path)
        config_dict = {key: value for key, value in config[section].items()}
        return cls(config_dict, default=default)

    @classmethod
    def from_file(
        cls, file: Union[str, os.PathLike], section: str = DEFAULTSECT, default=None
    ) -> "Configuration":
        """ Constructs a Configuration instance from a single INI file.
        """
        return cls.from_files(file, section=section, default=default)
