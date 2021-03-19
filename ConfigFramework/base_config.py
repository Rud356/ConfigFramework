from __future__ import annotations
from inspect import signature
from typing import Set, Type
from copy import deepcopy

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class BaseConfig:
    """
    Base class for configs you must inherit from if you want to write your own config class.

    """
    def __init__(self, *args, __passed_classes: Set[Type] = None, **kwargs):
        """
        Initializes config class.

        If you want to define variable as class, inherited from AbstractConfigVar - then its `__init__`
        must take no arguments and initialize everything inside (define the loader it takes var from,
        key with which you get to variable, etc.)

        :param args: args
        :param __passed_classes: set of classes, that already been initialized
        :param kwargs: kwargs
        """
        self._variables: Set[AbstractConfigVar] = set()
        self._loaders: Set[AbstractConfigLoader] = set()
        self._sub_configs: Set[BaseConfig] = set()

        self.__init_variables_of_config(args, kwargs, __passed_classes)
        self.__post_init__(*args, **kwargs)

    def __init_variables_of_config(self, args, kwargs, __passed_classes: Set[Type]):
        for key in dir(self):
            obj = getattr(self, key, None)

            if isinstance(obj, AbstractConfigVar):
                self._variables.add(obj)
                self._loaders.add(obj.loader)

            if obj.__class__ is type and AbstractConfigVar.__subclasscheck__(obj):
                params = list(signature(obj).parameters)
                if len(params) != 0:
                    raise ValueError(f"Parameters for {obj} initialization is not empty")

                initialized_var = deepcopy(obj)()
                self._variables.add(initialized_var)
                setattr(self, key,initialized_var)

            if issubclass(obj.__class__, BaseConfig):
                # initializing class with config underlying our main config
                # here's fix for possible circular class initialization
                __passed_classes.add(self.__class__)
                if obj in __passed_classes:
                    # should fix recursive config classes referencing
                    continue

                self.__dict__[key] = obj(*args, **kwargs, __passed_classes=__passed_classes)
                self._sub_configs.add(self.__dict__[key])

    def __post_init__(self, *args, **kwargs):
        """
        Post-initialization hook that receives all args and kwargs from initialization.

        :param args: arguments
        :param kwargs: keyword args
        :return:
        """
        pass

    def dump(self, include_defaults: bool = False):
        """
        Writes variables updated values to their.
        :param include_defaults:
        :return:
        """
        for loader in self._loaders:
            if loader.include_defaults is None:
                loader.dump(include_defaults)

            else:
                loader.dump(loader.include_defaults)

        for sub_config in self._sub_configs:
            sub_config.dump(include_defaults)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.__class__.__name__
