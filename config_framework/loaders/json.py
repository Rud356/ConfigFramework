import json
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Union, Optional, MutableMapping, Any, Callable

from config_framework.types.abstract import AbstractLoader


class Json(AbstractLoader):
    path: Union[PathLike, Path]
    encoding: str
    json_loader: Callable
    json_dumper: Callable

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any],
        path: Union[PathLike, Path],
        encoding: str,
        json_loader: Callable,
        json_dumper: Callable
    ):
        super().__init__(data, defaults)
        self.path = path
        self.encoding = encoding
        self.json_loader = json_loader
        self.json_dumper = json_dumper

    @classmethod
    def load(
        cls, path: Union[PathLike, Path],
        defaults: Optional[MutableMapping[str, Any]] = None,
        encoding: str = "utf8",
        json_loader=json.load,
        json_dumper=partial(json.dump, ensure_ascii=False, indent=4),
    ):
        with open(path, encoding=encoding) as data_f:
            data = json_loader(data_f)

        return cls(
            data=data, defaults=defaults or {},
            path=path, encoding=encoding,
            json_loader=json_loader, json_dumper=json_dumper
        )

    def dump(self, include_defaults: bool = False) -> None:
        to_dump = self.data
        if include_defaults:
            to_dump = dict(self.lookup_data)

        with open(self.path, 'w', encoding=self.encoding) as json_f:
            self.json_dumper(to_dump, json_f)
