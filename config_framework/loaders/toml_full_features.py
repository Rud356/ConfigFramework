from functools import partial
from os import PathLike
from pathlib import Path
from typing import Union, Optional, MutableMapping, Any, Callable, Dict

import toml as toml_loader_lib

from config_framework.loaders.toml_read_only import TomlReadOnly


class Toml(TomlReadOnly):
    path: Union[PathLike, Path]
    encoding: str
    toml_loader: Callable
    toml_dumper: Callable

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any],
        path: Union[PathLike, Path],
        encoding: str,
        toml_loader: Callable,
        toml_dumper: Callable
    ):
        super().__init__(data, defaults, path, encoding, toml_loader, toml_dumper)

    @classmethod
    def load(
        cls, path: Union[PathLike, Path],
        defaults: Optional[MutableMapping[str, Any]] = None,
        loader_kwargs: Optional[Dict[Any, Any]] = None,
        dumper_kwargs: Optional[Dict[Any, Any]] = None,
        encoding: str = "utf8",
    ):
        """
        Initializes loader for read only toml.

        :param path: path that is used to load config.
        :param defaults: default values.
        :param loader_kwargs: used for specifying parameters, according to toml documentation of `toml.load` function.
        :param dumper_kwargs: used for specifying parameters, according to toml documentation of `toml.dump` function.
        :param encoding: which encoding should be used for a file.
        :return: instance of TomlReadOnly class.
        """
        with open(path, encoding=encoding) as data_f:
            data = toml_loader_lib.load(data_f)

        if loader_kwargs is None:
            loader_kwargs = dict()

        if dumper_kwargs is None:
            dumper_kwargs = dict()

        return cls(
            data=data, defaults=defaults or {},
            path=path, encoding=encoding,
            toml_loader=partial(toml_loader_lib.load, **loader_kwargs),
            toml_dumper=partial(toml_loader_lib.dump, **dumper_kwargs)
        )

    def dump(self, include_defaults: bool = False) -> None:
        to_dump = self.data
        if include_defaults:
            to_dump = dict(self.lookup_data)

        with open(self.path, 'w', encoding=self.encoding) as json_f:
            self.toml_dumper(to_dump, json_f)
