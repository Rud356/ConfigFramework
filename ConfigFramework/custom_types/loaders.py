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
    @abstractmethod
    def __init__(self, data: Dict, defaults=None, *args, **kwargs):
        self.data: Dict = data

        if isinstance(defaults, dict):
            self.data = ChainMap(data, defaults)

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        pass

    @abstractmethod
    def dump(self):
        pass

    def dump_to_other_loader(self, other_loader: AbstractConfigLoader):
        other_loader.data = self.data
        other_loader = deepcopy(other_loader)
        other_loader.dump()

        return other_loader

    def set_variable(self, key: Hashable, value: Any):
        if key not in self.keys() and config.getboolean(
            "LoadersVariables", "AllowCreatingNotExistingKeys", fallback=False
        ):
            raise KeyError(f"This key doesn't exists in loader: {self}")

        self.data[key] = value

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def __getitem__(self, key: Hashable):
        return self.data[key]

    def __repr__(self):
        return f"Loader: {self.__class__.__name__}"

    def __str__(self):
        return self.__class__.__name__


class CompositeConfigLoader(AbstractConfigLoader):
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
        return cls(loaders)

    def dump(self, dump_specific_loader: AbstractConfigLoader = None):
        if not dump_specific_loader:
            for loader in self._config_loaders:
                loader.dump()

        else:
            dump_specific_loader.dump()

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

    def to_dict(self):
        keys = list(self.keys())
        keys.sort()

        items = {}
        for key in keys:
            items[key] = self[key]

        return items

    def keys(self):
        combined_keys = set()

        for loader in self._config_loaders:
            prepared_keys = set(loader.keys())
            combined_keys = combined_keys.union(prepared_keys)

        return combined_keys

    def values(self):
        return self.to_dict().keys()

    def items(self):
        self.to_dict().items()


class JSONFileConfigLoader(AbstractConfigLoader):
    dumper = partial(
        json.dump, ensure_ascii=False, check_circular=True,
        indent=config.getint("LoadersVariables", "JSONConfigLoader.dump_indent", fallback=4)
    )
    loader = partial(json.load, encoding='utf8')

    def __init__(self, filepath: Union[PathLike, str], defaults=None):

        self._config_path = filepath
        with open(filepath, encoding='utf8') as f:
            super().__init__(self.loader(f), defaults)

    @classmethod
    def load(cls, filepath: PathLike, defaults=None):
        return cls(filepath, defaults)

    def dump(self):
        with open(self._config_path, mode='w', encoding='utf8') as config_f:
            data = dict(self.data)
            self.dumper(data, config_f)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._config_path}"


class JSONStringConfigLoader(JSONFileConfigLoader):
    loader = json.loads
    dumper = partial(
        json.dumps, ensure_ascii=False, check_circular=True,
        indent=config.getint("LoadersVariables", "JSONConfigLoader.dump_indent", fallback=4)
    )

    def __init__(self, serialized: str, defaults=None):
        super(AbstractConfigLoader, self).__init__(self.loader(s=serialized), defaults)

    @classmethod
    def load(cls, serialized: str, defaults=None):
        return cls(serialized, defaults)

    def dump(self):
        return self.dumper(dict(self.data))

    def __str__(self):
        return f"{self.__class__.__name__}"


class YAMLConfigLoader(AbstractConfigLoader):
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
        with open(self._config_path) as config_f:
            self.dumper(config_f, self)

    def __str__(self):
        return f"{self.__class__.__name__}: {self._config_path}"


class EnvironmentConfigLoader(AbstractConfigLoader):
    def __init__(self, defaults=None):
        if not config.getboolean("LoadersVariables", "EnvironmentConfigLoader.mute_warning", fallback=False):
            logger.warn("Note that EnvironmentConfigLoader only dumps vars as str and you always have to set casters")
        super().__init__(dict(environ), defaults)

    def dump(self):
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
