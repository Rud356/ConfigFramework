from __future__ import annotations

from abc import ABC, abstractmethod
from collections import ChainMap, Mapping
from functools import lru_cache
from pathlib import Path
from time import time
from typing import Any, AnyStr, Dict, Hashable, NoReturn, Optional, Tuple, Union


class AbstractConfigLoader(ABC, Mapping):
    """
    Base class for any of your loaders. Initialization can be made through load function, or, if author wants so,
    through `__init__` function.
    """

    def __init__(
        self, data: Union[Dict, ChainMap, Mapping], defaults: Dict, include_defaults_to_dumps: Optional[bool] = None,
        *args, **kwargs
    ):
        """
        Creates new config first_loader with your variables.

        :param data: data from first_loader.
        :param defaults: default variables that will be used if not found in first_loader.
        :param include_defaults_to_dumps: represents if default values should be dumped to that first_loader.
        :param args: arguments that can be used for your custom loaders.
        :param kwargs: keyword arguments that can be used for your custom loaders.
        """
        self.__created_at = str(time())
        self.data = data
        self.include_defaults: bool = include_defaults_to_dumps
        self.defaults = defaults

        if isinstance(defaults, dict):
            self.lookup_data = ChainMap(self.data, self.defaults)

        else:
            self.lookup_data = self.data

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        """
        Initializes creation of new ConfigLoader.
        You must provide your arguments that are needed for your first_loader.

        :param args: arguments that can be used for your custom loaders.
        :param kwargs: keyword arguments that can be used for your custom loaders.
        """
        pass

    @abstractmethod
    def dump(self, include_defaults: bool = False) -> NoReturn:
        """
        Dumps updated variables to loader.

        :param include_defaults: specifies if you want to have default variables to be dumped.
        :return: nothing.
        """
        pass

    def dump_to(self, other_loader: AbstractConfigLoader, include_defaults: bool = False) -> NoReturn:
        """
        Dumps variables to other first_loader that been already initialized.

        :param other_loader: other first_loader that already initialized and where you want to dump stuff.
        :param include_defaults: include_defaults_to_dumps: specifies if you want to have default variables to be.
        :return: nothing.
        """
        if isinstance(other_loader, AbstractConfigLoader):
            if include_defaults:
                other_loader.lookup_data = self.lookup_data

            else:
                other_loader.lookup_data = self.data

        else:
            raise ValueError(
                f"{self} got invalid first_loader to dump variables to. Got type: {type(other_loader)}"
            )

        other_loader.dump(include_defaults)

    def get(self, key: Union[Hashable, AnyStr], default=None) -> Any:
        """
        Returns an item under specified key or key as path and if
        it didn't find it - returns default variable.

        :param key: a key that points at where you want to grab variable.
        :param default: default config_var.
        :return: anything lying there.
        """
        casted_key = self.key_to_path_cast(key)
        val_root = self.get_to_variable_root(casted_key)

        return val_root.get(casted_key[-1], default)

    @staticmethod
    @lru_cache(maxsize=None)
    def key_to_path_cast(key: Union[AnyStr, Hashable]) -> Union[Tuple[AnyStr, ...], Tuple[Hashable, ...]]:
        """
        Casts a key to tuple of keys, that should be applied one by one to get to where variable lies.
        Path pointing example: config_root/database/database_ip

        :param key: string with path, pointing at out variable or hashable.
        :return: tuple of sub keys.
        """
        if isinstance(key, str) and ("/" in key):
            return Path(key).parts

        return key,

    def get_to_variable_root(
        self, keys: Union[Tuple[AnyStr, ...], Tuple[Hashable, ...]], lookup_at: Optional[Dict] = None
    ) -> Dict:
        """
        Returns an dictionary with our variable.

        :param keys: keys tuple we apply to get to root of variable.
        :param lookup_at: the location we're looking at. In case we need to lookup at specific part of our first_loader.
        :return: a dictionary which layer should contain our variable.
        """
        root = lookup_at or self.lookup_data
        # Last part of key must be the variable
        for key in keys[:-1]:
            root = root[key]

        return root

    def __getitem__(self, key: Union[Hashable, AnyStr]) -> Any:
        """
        Returns an item under specified key or key as path and if
        it didn't find it - raises KeyError.

        :param key: variable key.
        :return: value.
        """
        casted_key = self.key_to_path_cast(key)
        val_root = self.get_to_variable_root(casted_key)

        return val_root[casted_key[-1]]

    def __setitem__(self, key: Union[Hashable, AnyStr], value: Any) -> NoReturn:
        """
        Sets variable config_var inside of your first_loader.

        :param key: a key that points at what variable you want to set config_var to.
        :param value: a new config_var for variable.
        :return: nothing.
        """

        casted_key = self.key_to_path_cast(key)
        val_root = self.get_to_variable_root(casted_key)

        if casted_key[-1] not in val_root:
            raise KeyError(f"No key {casted_key[-1]} in {self}")

        val_root[casted_key[-1]] = value

    def __hash__(self):
        return hash(self.__class__.__name__ + self.__created_at)

    def __repr__(self):
        return f"Loader: {self.__class__.__name__}"

    def __str__(self):
        return self.__class__.__name__

    def __len__(self) -> int:
        return len(self.lookup_data)

    def __iter__(self):
        return iter(self.lookup_data)


__all__ = ["AbstractConfigLoader"]
