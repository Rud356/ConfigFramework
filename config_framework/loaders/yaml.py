import yaml
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Union, Optional, MutableMapping, Any, Callable

from config_framework.types.abstract import AbstractLoader

try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    # Those are actually replacements for CDumper/CLoader
    # and so there must be no problem
    from yaml import Loader, Dumper  # type: ignore


class Yaml(AbstractLoader):
    path: Union[PathLike, Path]
    encoding: str
    yaml_loader: Callable
    yaml_dumper: Callable

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any],
        path: Union[PathLike, Path],
        encoding: str,
        yaml_loader: Callable,
        yaml_dumper: Callable
    ):
        super().__init__(data, defaults)
        self.path = path
        self.encoding = encoding
        setattr(self, "yaml_loader", yaml_loader)
        setattr(self, "yaml_dumper", yaml_dumper)

    @classmethod
    def load(
        cls, path: Union[PathLike, Path],
        defaults: Optional[MutableMapping[str, Any]] = None,
        encoding: str = "utf8",
        yaml_loader=partial(yaml.load, Loader=Loader),
        yaml_dumper=partial(yaml.dump, Dumper=Dumper),
    ):
        """
        Loads yaml from file.

        :param path: where is yaml file to load data from.
        :param defaults: default values for config.
        :param encoding: which encoding does config file has (defaults to utf-8).
        :param yaml_loader: function that is used for loading data from file.
        :param yaml_dumper: function that is used for saving data to file.
        :return: instance of yaml loader.
        """
        with open(path, encoding=encoding) as data_f:
            data = yaml_loader(data_f)

        return cls(
            data=data, defaults=defaults or {},
            path=path, encoding=encoding,
            yaml_loader=yaml_loader,
            yaml_dumper=yaml_dumper
        )

    def dump(self, include_defaults: bool = False) -> None:
        to_dump = self.data
        if include_defaults:
            to_dump = dict(self.lookup_data)

        with open(self.path, 'w', encoding=self.encoding) as yaml_f:
            self.yaml_dumper(data=to_dump, stream=yaml_f)
