from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections import ChainMap
from copy import deepcopy
from functools import partial
from os import PathLike, environ
from typing import Dict, Any, Hashable, Tuple, Union

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from . import logger, config


class AbstractConfigLoader(ABC):
    """
    A base class of which all config loaders must be created

    To initialize any config loader it's recommended to use *load* function
    """

    def __init__(self, data: Dict, defaults: dict = None, *args, **kwargs):
        """
        Basic init for any config loader as well can be reused for any of yours loaders.
        In *load* function you may prepare your data to be a dict and the pass it as data param, which will be useful.

        :param data: dict - all vars as dict loaded from config source
        :param defaults: dict - default variables for our config source
        :param args: Any - anything you might need too
        :param kwargs: Any - anything you might need
        """
        self.data: Dict = data

        if isinstance(defaults, dict):
            self.data = ChainMap(data, defaults)

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        """
        Function to do anything before passing your data to init.
        You might even fetch config from internet or start a rocker :)

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Function that saves all data back to place from where it was loaded with applying *dump_caster* on data.

        :return:
        """
        pass

    def dump_to_other_loader(self, other_loader: AbstractConfigLoader) -> AbstractConfigLoader:
        """
        Dumps data to copied loader (creates deep copy of it) and returning it.

        :param other_loader: AbstractConfigLoader - any other loader
        :return: AbstractConfigLoader
        """
        other_loader.data = self.data
        other_loader = deepcopy(other_loader)
        other_loader.dump()

        return other_loader

    def set_variable(self, key: Hashable, value: Any):
        """
        Sets value to a key inside specific loader. If option `AllowCreatingNotExistingKeys` (defaults to False)
        is set to False - it won't let you create variables, which keys were not defined in loader.

        :param key: Hashable
        :param value: Any
        :return: None
        """
        if key not in self.keys() and config.getboolean(
            "LoadersVariables", "AllowCreatingNotExistingKeys", fallback=False
        ):
            raise KeyError(f"This key doesn't exists in loader: {self}")

        self.data[key] = value

    def keys(self) -> dict.keys:
        """
        Returns all loaders keys.

        :return: Any
        """
        return self.data.keys()

    def values(self) -> dict.values:
        """
        Returns all loaded values

        :return: Any
        """
        return self.data.values()

    def items(self) -> dict.items:
        """
        Returns all loaded (key, item).

        :return: Any
        """
        return self.data.items()

    def __getitem__(self, key: Hashable) -> Any:
        """
        Returns a value behind specified key. Raises KeyError if not found.

        :param key: Hashable
        :return: Any
        """
        return self.data[key]

    def __repr__(self):
        return f"Loader: {self.__class__.__name__}"

    def __str__(self):
        return self.__class__.__name__


class CompositeConfigLoader(AbstractConfigLoader):
    """
    Combines keys from multiple ConfigLoaders and giving one interface to access them.
    Might be helpful if you want to use multiple providers and have priority when deciding what variable value to use
    if it exists in many configs. Searching vars in left to right order.
    """

    def __init__(self, loaders: Tuple[AbstractConfigLoader]):
        super().__init__({})
        self._config_loaders = loaders

    def dump_to_other_loader(self, other_loader: AbstractConfigLoader):
        data = self.to_dict()
        other_loader = deepcopy(other_loader)
        other_loader.data = data
        other_loader.dump()

        return other_loader

    def _get_key_from_loader(self, key: Hashable, loader: AbstractConfigLoader):
        """
        Trying to get a key from specific loader.
        If not found - raises KeyError and telling inside which loader it was.

        :param key:
        :param loader:
        :return:
        """
        if key in loader.keys():
            return loader[key]

        raise KeyError(f"No key in loader {loader}")

    def __getitem__(self, key: Hashable):
        value = None
        found_value = False

        for loader in self._config_loaders:
            try:
                temp_val = self._get_key_from_loader(key, loader)

            except KeyError:
                continue

            else:
                value = temp_val
                found_value = True
                break

        if not found_value:
            raise KeyError(
                f"Loader {self.__name__} don't have specified key in any of sub-loaders: {key}"
                "\n".join((str(sub_loader) for sub_loader in self._config_loaders))
            )

        return value

    @classmethod
    def load(cls, *loaders: AbstractConfigLoader):
        """
        Initializes CompositeConfigLoader that will get variables from all listed loaders.
        Search happening from first to last element and giving a first value that been found.

        :param loaders: AbstractConfigLoader
        :return: - cls
        """
        return cls(loaders)

    def dump(self, dump_specific_loader: AbstractConfigLoader = None):
        """
        Dumps variables to their specific loader by default. If specified what loader it should dump to - it will not
        dump any other loader which might save some time.

        :param dump_specific_loader: Optional[AbstractConfigLoader]
        :return:
        """
        if not dump_specific_loader:
            for loader in self._config_loaders:
                loader.dump()

        else:
            return dump_specific_loader.dump()

    def set_variable(self, key: Hashable, value: Any):
        for loader in self._config_loaders:
            try:
                self._get_key_from_loader(key, loader)

            except KeyError:
                continue

            else:
                updating_loader: AbstractConfigLoader = loader
                break

        else:
            raise KeyError(
                "No such key in any of loaders:"
                "\n".join((str(loader) for loader in self._config_loaders))
            )

        updating_loader.set_variable(key, value)

    def to_dict(self) -> dict:
        """
        Returns dict with merged keys

        :return:
        """
        keys = list(self.keys())
        keys.sort()

        items = {}
        for key in keys:
            items[key] = self[key]

        return items

    def keys(self) -> dict.keys:
        combined_keys = set()

        for loader in self._config_loaders:
            prepared_keys = set(loader.keys())
            combined_keys = combined_keys.union(prepared_keys)

        return combined_keys

    def values(self) -> dict.values:
        return self.to_dict().keys()

    def items(self) -> dict.items:
        self.to_dict().items()


class JSONFileConfigLoader(AbstractConfigLoader):
    """
    JSON config loader from files. You might change load and dump functions by writing in your code:

    JSONFileConfigLoader.dumper = json.alt_dumper
    JSONFileConfigLoader.loader = json.alt_loader

    Might be useful if you want to apply your dumper which might be faster or can cast your types to json.
    """
    dumper = partial(
        json.dump, ensure_ascii=False, check_circular=True,
        indent=config.getint("LoadersVariables", "JSONConfigLoader.dump_indent", fallback=4)
    )
    loader = partial(json.load)

    def __init__(self, filepath: Union[PathLike, str], defaults=None):

        self._config_path = filepath
        with open(filepath, encoding='utf8') as f:
            super().__init__(self.loader(f), defaults)

    @classmethod
    def load(cls, filepath: Union[PathLike, str], defaults=None):
        return cls(filepath, defaults)

    def dump(self):
        with open(self._config_path, mode='w', encoding='utf8') as config_f:
            data = dict(self.data)
            self.dumper(data, config_f)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._config_path}"


class JSONStringConfigLoader(JSONFileConfigLoader):
    """
    JSON config loader from strings. You might change load and dump functions by writing in your code:

    JSONStringConfigLoader.dumper = json.alt_dumper
    JSONStringConfigLoader.loader = json.alt_loader

    Might be useful if you want to apply your dumper which might be faster or can cast your types to json.
    """
    loader = partial(json.loads)
    dumper = partial(
        json.dumps, ensure_ascii=False, check_circular=True,
        indent=config.getint("LoadersVariables", "JSONConfigLoader.dump_indent", fallback=4)
    )

    def __init__(self, serialized: str, defaults=None):
        data = self.loader(serialized)
        self.data: Dict = data

        if isinstance(defaults, dict):
            self.data = ChainMap(data, defaults)

    @classmethod
    def load(cls, serialized: str, defaults=None):
        return cls(serialized, defaults)

    def dump(self):
        return self.dumper(dict(self.data))

    def __str__(self):
        return f"{self.__class__.__name__}"


class YAMLConfigLoader(AbstractConfigLoader):
    """
    YAML config loader from files. You might change load and dump functions by writing in your code:

    YAMLConfigLoader.dumper = yaml.alt_dumper
    YAMLConfigLoader.loader = yaml.alt_loader

    Might be useful if you want to apply your dumper which might be faster or can cast your types to json.
    """
    dumper = partial(yaml.dump, Dumper=Dumper)
    loader = partial(yaml.load, Loader=Loader)

    def __init__(self, filepath: Union[PathLike, str], defaults=None):
        self._config_path = filepath
        with open(filepath, encoding='utf8') as f:
            super().__init__(self.loader(f), defaults)

    @classmethod
    def load(cls, filepath: PathLike, defaults=None):
        return cls(filepath, defaults)

    def dump(self):
        with open(self._config_path, mode='w', encoding='utf8') as config_f:
            self.dumper(self.data, config_f)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._config_path}"


class EnvironmentConfigLoader(AbstractConfigLoader):
    def __init__(self, defaults=None):
        if not config.getboolean("LoadersVariables", "EnvironmentConfigLoader.mute_warning", fallback=False):
            logger.warn("Note that EnvironmentConfigLoader only dumps vars as str and you always have to set casters")
        super().__init__(dict(environ), defaults)

    def dump(self):
        """
        Dump function is here left for compatibility with AbstractConfigLoader interface, nothing else. You can't really
        dump anything to env vars because they are being set immediately.

        :return:
        """
        pass

    @classmethod
    def load(cls):
        return cls()

    def set_variable(self, key: str, value: str, **_):
        self.data[key] = str(value)
        environ[key] = str(value)


__all__ = (
    "AbstractConfigLoader", "CompositeConfigLoader", "JSONFileConfigLoader", "JSONStringConfigLoader",
    "YAMLConfigLoader", "EnvironmentConfigLoader"
)
