from __future__ import annotations

import os
from configparser import ConfigParser, DEFAULTSECT
from inspect import isclass
from pathlib import Path
from typing import Iterator, Union

DEFAULT_VALUE_PLACEHOLDER = object()


class Configuration:
    """Main Configuration class."""

    def __init__(self, config: dict, default=None):
        self._config = {key.lower(): value for key, value in config.items()}
        self._default = default

    def __getattr__(self, item: str):
        return self.get(item)

    def get(self, key: str, default=DEFAULT_VALUE_PLACEHOLDER):
        """Retrieves a single configuration value.

        Args:
            key: The key of the value to retrieve.
            default: The default value in case the key does not exist.

        Returns:
            Depending on the type of the value under the key:
              * If the value is an Exception class, it's raised.
              * If the value is a callable, it's called with `key` as the only argument, and
                the result of that call is then returned.
              * Otherwise, the value is returned as-is.
        """
        if default is DEFAULT_VALUE_PLACEHOLDER:
            default = self._default
        value = self._config.get(key.lower(), default)
        if isclass(value) and issubclass(value, BaseException):
            raise value(f"{key} is not defined")
        if callable(value):
            return value(key)
        return value

    def __iter__(self) -> Iterator[tuple]:
        """Returns an iterator of keys/value pairs."""
        yield from self._config.items()

    @classmethod
    def from_environ(
        cls, prefix: str, remove_prefix: bool = False, default=None
    ) -> Configuration:
        """
        Constructs a Configuration instance from a set of environment variables.

        Args:
            prefix: Only the variables starting with the prefix will be included.
            remove_prefix: If true, the configuration values will not include the prefic. For
                           example, `PREFIX_FOO_BAR` will become `FOO_BAR`.
            default: The default value for an undefined variable.

        Returns:
            A Configuration instance.
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
    ) -> Configuration:
        """
        Constructs a Configuration instance from one or more INI files.

        Each file is expected to be compatible with the ConfigParser module.

        Args:
            *files: Positional arguments are the paths to the configuration files.
            section: The section to use to read keys and values.
            default: The default value for an undefined variable.

        Returns:
            A Configuration instance.
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
    ) -> Configuration:
        """
        Constructs a Configuration instance from a single INI file.

        The file is expected to be compatible with the ConfigParser module.

        Args:
            files: The path to the configuration files.
            section: The section to use to read keys and values.
            default: The default value for an undefined variable.

        Returns:
            A Configuration instance.
        """
        return cls.from_files(file, section=section, default=default)
