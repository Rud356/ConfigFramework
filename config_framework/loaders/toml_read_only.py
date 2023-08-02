import tomllib as toml_loader_lib
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Union, Optional, MutableMapping, Any, Callable, Dict

from config_framework.types.abstract import AbstractLoader


class TomlReadOnly(AbstractLoader):
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
        super().__init__(data, defaults)
        self.path = path
        self.encoding = encoding
        setattr(self, "toml_loader", toml_loader)
        setattr(self, "toml_dumper", toml_dumper)

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
        :param loader_kwargs: used for specifying parameters, according to tomllib documentation of `tomllib.load`
            function.

        :param dumper_kwargs: not used.
        :param encoding: which encoding should be used for a file.

        :return: instance of TomlReadOnly class.
        """
        with open(path, encoding=encoding, mode="b") as data_f:
            data = toml_loader_lib.load(data_f)

        if loader_kwargs is None:
            loader_kwargs = dict()

        return cls(
            data=data, defaults=defaults or {},
            path=path, encoding=encoding,
            toml_loader=partial(toml_loader_lib.load, **loader_kwargs),
            toml_dumper=lambda *args, **kwargs: None  # it doesn't work for this class
        )

    def dump(self, include_defaults: bool = False) -> None:
        raise RuntimeError(
            "You don't have dependency installed to write to toml files."
        )
