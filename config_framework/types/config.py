from __future__ import annotations

from typing import Set

from .abstract.loader import AbstractLoader
from .variable import Variable


class BaseConfig:
    frozen: bool
    _variables: Set[Variable]
    _loaders: Set[AbstractLoader]

    def __init__(self, frozen: bool = True):
        """
        Initializes config class.

        :param frozen: prevents user from assigning any values directly
            to class instance. Object will be not modifiable after
            __post_init__ is called.
        :return: nothing.
        """
        self.frozen = False
        self.__post_init__()
        self.frozen: bool = frozen

    def __post_init__(self) -> None:
        """
        Function with custom user actions for any purpose.

        :return: nothing.
        """
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        """
        Function that collects all variables and loaders from inherited config.

        :kwargs: subclasses kwargs.
        :return: nothing.
        """
        cls._loaders = set()
        cls._variables = set()

        for key, value in cls.__dict__.items():
            if isinstance(value, Variable):
                cls._variables.add(value)
                cls._loaders.add(value.source)

    def __setattr__(self, key, value):
        """
        Assigns value to class under specific key.

        :param key: attribute key.
        :param value: attribute value.
        :return: nothing.
        """
        is_frozen = getattr(self, "frozen", False)

        if key is 'frozen':
            super().__setattr__(key, value)

        elif not is_frozen:
            super().__setattr__(key, value)

        else:
            raise NotImplementedError(
                "This instance can't have anything assigned"
            )

    def save(self, include_defaults: bool = True) -> None:
        """
        Saves updated variables values to some storage using
            AbstractLoader.dump method.

        :param include_defaults: if dump of config must include default values.
        :return: nothing.
        """
        for loader in self._loaders:
            loader.dump(include_defaults)

    def __repr__(self):
        return self.__class__.__name__
