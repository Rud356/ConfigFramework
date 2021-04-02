from __future__ import annotations
from functools import wraps
from typing import Any, AnyStr, Callable, Hashable, NoReturn, Optional, TYPE_CHECKING, Type
from ConfigFramework.loaders.composite_loader import CompositeLoader

if TYPE_CHECKING:
    from .abc_loader import AbstractConfigLoader
    from ConfigFramework.dump_caster import DumpCaster


class AbstractConfigVar:
    """
    Abstract config variable with descriptors interface which is a base type for any of your variables classes.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        typehint: Optional[Type] = Any,
        caster: Optional[Callable] = None, dump_caster: Optional[Callable, DumpCaster] = None,
        validator: Optional[Callable] = None, default: Optional[Any] = None, constant: bool = False
    ):
        """
        Initializes variable for specified first_loader and key.

        :param key: Any hashable or a string. Strings can be written as paths in case you need a variable.
         that underlies other mappings. Example of how to get such vars: `config_root/database/database_ip`.
        :param loader: A first_loader that will be looked up to get vars config_var or to update values.
        :param typehint: Typehint for __value field, that by default being returned.
        :param caster: Callable that should return variable casted to specific type (in case you need custom types).
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster
        :param validator: Callable that validates config_var or defaults in case the original config_var is invalid.
        :param default: Default config_var that will be set, if config_var is invalid.
        :param constant: Sets if variable config_var can be set in runtime
        """
        self.key = key
        self.is_constant = constant
        self.loader: AbstractConfigLoader = loader
        self.__post_init = False

        # Redefining functions that we will need if they are provided
        for redefine_func_name, func in zip(
            ("caster", "dump_caster", "validate"),
            (caster, dump_caster, validator)
        ):
            if callable(func):
                setattr(self, redefine_func_name, func)

        if default is not None:
            self.__value: typehint = self.caster(loader.get(key, default))
            default = self.caster(default)

        else:
            self.__value: typehint = self.caster(loader[key])

        # Validation of config_var and defaults
        bool_casted_validator: Callable = self._validate_to_bool(self.validate)

        if not bool_casted_validator(self.__value):
            if (default is not None) and bool_casted_validator(default):
                self.__value: typehint = default

            elif self._validate_value_in_defaults(self.validate, self.caster, loader, key):
                key = loader.key_to_path_cast(key)
                var_key = loader.key_to_path_cast(key)

                self.value: typehint = loader.get_to_variable_root(key, lookup_at=loader.defaults)[var_key]

            else:
                raise ValueError(f"Invalid config_var for {self} in {self.loader} and default values not found")

        self.__post_init = True

    def caster(self, value: Any) -> Any:
        """
        Callable that should return variable casted to specific type (in case you need custom types).

        :param value: config_var to be casted.
        :return: value casted to whatever type you need.
        """
        return value

    def dump_caster(self, config_var: AbstractConfigVar) -> Any:
        """
        Callable that being called when config being dumped.
        Nothing being passed as attribute since it should be executed after assigning the config_var to ConfigVar.

        Through self we can obtain access to useful stuff and also use DumpCaster, which allows us to assign
        specific caster for exact ConfigLoader.
        :return: value casted to whatever type you need to save value.
        """
        return config_var.__value

    def validate(self, value: Any) -> bool:  # noqa
        """
        Callable that validates config_var or defaults in case the original config_var is invalid.

        :param value: config_var to be validated.
        :return: bool value representing if variable has a valid value.
        """
        return True

    def _loader_type(self) -> Type[AbstractConfigLoader]:
        """
        Internal function that helps us to find from what exact first_loader we got var from.

        :return: loader class.
        """
        if not isinstance(self.loader, CompositeLoader):
            return type(self.loader)

        else:
            self.loader: CompositeLoader
            for loader in self.loader.loaders:
                try:
                    loader[self.key]

                except KeyError:
                    continue

                else:
                    return type(loader)

    @staticmethod
    def _validate_to_bool(func):
        """
        Wrapper that returns a bool config_var representing if check failed or raised ValueError.

        :param func: function that is wrapped for specific validator. Will be used in checking if value is correct
        to apply defaults.
        :return: callable.
        """
        @wraps(func)
        def execute(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ValueError:
                return False

        return execute

    @staticmethod
    def _validate_value_in_defaults(validator: Callable, caster: Callable, loader: AbstractConfigLoader, key) -> bool:
        if not hasattr(loader, 'defaults'):
            return False

        bool_casted_validator: Callable = AbstractConfigVar._validate_to_bool(validator)
        *keys, variable_key = loader.key_to_path_cast(key)

        try:
            variable_root = loader.get_to_variable_root(keys, lookup_at=loader.defaults)
            variable = variable_root[variable_key]

        except KeyError:
            return False

        return bool_casted_validator(caster(variable))

    @property
    def value(self) -> Any:
        """
        Gives access to casted value.

        :return: any value from config, that been casted and validated.
        """
        return self.__value

    @value.setter
    def value(self, value: Any) -> NoReturn:
        """
        Sets a new value to config variable and updates its value in loader with casting it to needed type.

        :param value: a new value to be set and validated.
        :return: nothing.
        """
        if self.is_constant and self.__post_init:
            raise NotImplementedError("Constants can not be assigned in runtime")

        if not self.validate(value):
            raise ValueError(f"Invalid config_var to be set for property {self}")

        self.__value = value
        self.loader[self.key] = self.dump_caster(self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.key} in {self.loader} = {self.__value}"


__all__ = ["AbstractConfigVar"]
