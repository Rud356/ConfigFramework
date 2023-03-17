from __future__ import annotations

import abc
from collections import ChainMap
from time import time
from typing import MutableMapping, Any, Union, Optional

from ..variable_key import VariableKey


class AbstractLoader(MutableMapping, abc.ABC):
    """
    Class that is used as configuration data source.
    """
    data: MutableMapping[str, Any]
    defaults: MutableMapping[str, Any]

    lookup_data: MutableMapping[str, Any]
    __created_at: str

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any]
    ):
        # Fixes errors when loader returns None from empty file or smt like that
        if data is None:
            data = {}

        self.data = data
        self.defaults = defaults

        self.__created_at: str = str(time())
        self.lookup_data: ChainMap = ChainMap(self.data, self.defaults)

    def get(
        self, key: Union[VariableKey, str],
        default: Optional[Any] = None
    ) -> Any:
        """
        Gives a value under specific key and if not found
        gives default value.

        :return: anything.
        """
        try:
            return self[key]

        except KeyError:
            return default

    def __getitem__(self, key: Union[VariableKey, str]) -> Any:
        """
        Returns an item under specified key.

        :param key: key that is used to find an item.
        :return: any value.

        :raises KeyError: if corresponding item wasn't found
            raises KeyValue with details
            about which key was used and what part of it wasn't found.
        """
        if isinstance(key, str):
            key = VariableKey(key)

        variable: Any = self.lookup_data
        for sub_key in key:
            try:
                variable = variable[sub_key]

            except KeyError as key_error:
                raise KeyError(
                    f"Couldn't find any value using key: {key}"
                ) from key_error

        return variable

    def __setitem__(self, key: Union[VariableKey, str], value: Any) -> None:
        """
        Sets an item value under specified key.
        :param key: key that is used to find an item.
        :return: any value.
        :raises KeyError: if corresponding item wasn't found
            raises KeyError with details
            about which key was used and what part of it wasn't found.
        """
        if isinstance(key, str):
            key = VariableKey(key)

        variable: MutableMapping[str, Any] = self.lookup_data
        key_as_tuple = tuple(key)
        for sub_key in key_as_tuple[:-1]:
            try:
                variable = variable[sub_key]

            except KeyError as key_error:
                raise KeyError(
                    f"Couldn't find any value using key: {key}"
                ) from key_error

        variable_key = key_as_tuple[-1]
        if variable_key not in variable:
            raise KeyError(
                f"There's no such key in loader: {key}"
            )
        variable[variable_key] = value

    @abc.abstractmethod
    def dump(self, include_defaults: bool = False) -> None:
        """
        Method that is used to dump all values to some storage.

        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.
        """
        pass

    def dump_to(
        self, other_loader: AbstractLoader,
        include_defaults: bool = False
    ) -> None:
        """
        Assigns data and defaults values from itself to other
        loader and then calling dump method with provided include_defaults
        value.

        :param other_loader: other initialized loader.
        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.

        :raises ValueError: if received not
            an instance of AbstractLoader subclass.
        """
        if isinstance(other_loader, AbstractLoader):
            if include_defaults:
                other_loader.defaults = self.defaults

            other_loader.data = self.data
            other_loader.lookup_data = ChainMap(
                other_loader.data,
                other_loader.defaults
            )
            other_loader.dump(include_defaults)

        else:
            raise ValueError(
                f"{self} got invalid other_loader "
                f"to dump variables to. Got type: {type(other_loader)}"
            )

    def __str__(self) -> str:
        return self.__class__.__name__

    def __delitem__(self, key: Union[str, VariableKey]) -> None:
        """
        Deletes value from loader by VariableKey.

        :param key: the key that must be deleted from loader.
        :return: nothing.
        """
        if isinstance(key, str):
            key = VariableKey(key)

        variable: Any = self.lookup_data
        key_as_tuple = tuple(key)
        for sub_key in key_as_tuple[:-1]:
            try:
                variable = variable[sub_key]

            except KeyError as key_error:
                raise KeyError(
                    f"Couldn't find any value using key: {key}"
                ) from key_error

        variable_key = key_as_tuple[-1]
        del variable[variable_key]

    def __len__(self) -> int:
        return len(self.lookup_data)

    def __iter__(self):
        return iter(self.lookup_data)

    def __hash__(self):
        return hash(str(self) + self.__created_at)
