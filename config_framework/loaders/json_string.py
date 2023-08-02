import json
from functools import partial
from typing import Optional, MutableMapping, Any, Callable

from config_framework.types.abstract import AbstractLoader


class JsonString(AbstractLoader):
    json_loader: Callable = json.load
    json_dumper: Callable = partial(json.dump, ensure_ascii=False, indent=4)

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any],
        encoding: str,
        json_loader: Callable,
        json_dumper: Callable
    ):
        super().__init__(data, defaults)
        self.encoding = encoding
        setattr(self, "json_loader", json_loader)
        setattr(self, "json_dumper", json_dumper)

    @classmethod
    def load(
        cls,
        data_string: str,
        encoding: str = "utf8",
        defaults: Optional[MutableMapping[str, Any]] = None,
        json_loader=json.loads,
        json_dumper=partial(json.dumps, ensure_ascii=False, indent=4),
    ):
        """
        Loads json file from path into loader.

        :param data_string: string with valid json formatted text.
        :param defaults: default values.
        :param encoding: which encoding does config file has (defaults to utf-8).
        :param json_loader: function that loads json from string.
        :param json_dumper: function that dumps to json string.
        :return: instance of json string loader.
        """
        data = json_loader(data_string)

        return cls(
            data=data, defaults=defaults or {}, encoding=encoding,
            json_loader=json_loader, json_dumper=json_dumper
        )

    def dump(self, include_defaults: bool = False) -> None:
        """
        This method doesn't change anything at all
        because strings are unchangeable.

        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.
        """
        pass
