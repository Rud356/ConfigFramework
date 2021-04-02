from __future__ import annotations

from typing import Optional, Set, Type, NoReturn

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class BaseConfig:
    """
    Base class for configs you must inherit from if you want to write your own config class.

    """
    def __init__(self, *args, __passed_classes: Set[Type] = None, **kwargs):
        """
        Initializes config class.

        :param args: args.
        :param __passed_classes: set of classes, that already been initialized.
        :param kwargs: kwargs.
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

            if type(obj) is type and BaseConfig.__subclasscheck__(obj):
                # initializing class with config underlying our main config
                # here's fix for possible circular class initialization
                if __passed_classes is None:
                    __passed_classes = set()

                __passed_classes.add(self.__class__)
                if obj in __passed_classes:
                    # should fix recursive config classes referencing
                    continue

                self.__dict__[key] = obj(*args, **kwargs, __passed_classes=__passed_classes)
                self._sub_configs.add(self.__dict__[key])

    def __post_init__(self, *args, **kwargs) -> NoReturn:
        """
        Post-initialization hook that receives all args and kwargs from initialization.

        :param args: arguments.
        :param kwargs: keyword args.
        :return: nothing.
        """
        pass

    def dump(self, include_defaults: Optional[bool] = None) -> NoReturn:
        """
        Writes variables updated values to their.

        :param include_defaults: represents dumping argument for all first_loader.
            In case you want to stay with including defaults defined
            by first_loader class - leave None config_var.

        :return: nothing.
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
