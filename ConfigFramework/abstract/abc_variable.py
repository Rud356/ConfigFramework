from __future__ import annotations
from abc import ABC
from functools import wraps
from typing import Any, AnyStr, Callable, Hashable, NoReturn, Optional, TYPE_CHECKING, Type

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
        Initializes variable for specified loader and key.

        :param key: Any hashable or a string. Strings can be written as paths in case you need a variable.
         that underlies other mappings. Example of how to get such vars: `config_root/database/database_ip`.
        :param loader: A loader that will be looked up to get vars value or to update values.
        :param typehint: Typehint for _value field, that by default being returned.
        :param caster: Callable that should return variable casted to specific type (in case you need custom types).
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster
        :param validator: Callable that validates value or defaults in case the original value is invalid.
        :param default: Default value that will be set, if value is invalid.
        :param constant: Sets if variable value can be set in runtime
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
                self.__dict__[redefine_func_name] = func

        if default is not None:
            self._value: typehint = self.caster(loader.get(key, default))
            default = caster(default)

        else:
            self._value: typehint = self.caster(loader[key])

        # Validation of value and defaults
        bool_casted_validator: Callable = self._validate_to_bool(self.validate)

        if not bool_casted_validator(self._value):
            if (default is not None) and self._validate_to_bool(self.validate(default)):
                self._value: typehint = default

            elif (
                (getattr(loader, "defaults", None) is not None) and
                bool_casted_validator(
                    caster(loader.get_to_variable_root(
                        loader.key_to_path_cast(key),
                        lookup_at=loader.defaults
                    ))
                )
            ):
                self._value: typehint = caster(loader.get_to_variable_root(
                    loader.key_to_path_cast(key), lookup_at=loader.defaults
                ))

            else:
                raise ValueError(f"Invalid value for {self} in {self.loader} and default values not found")

        self.__post_init = True

    def caster(self, value: Any) -> Any:
        """
        Callable that should return variable casted to specific type (in case you need custom types).

        :param value: value to be casted
        :return:
        """
        return value

    def dump_caster(self) -> Any:
        """
        Callable that being called when config being dumped.
        Nothing being passed as attribute since it should be executed after assigning the value to ConfigVar.

        Through self we can obtain access to useful stuff and also use DumpCaster, which allows us to assign
         specific caster for exact ConfigLoader
        :return:
        """
        return self._value

    def validate(self, value: Any) -> bool:  # noqa
        """
        Callable that validates value or defaults in case the original value is invalid.
        :param value: value to be validated
        :return:
        """
        return True

    @staticmethod
    def _validate_to_bool(func):
        """
        Wrapper that returns a bool value representing if check failed or raised ValueError.

        :param func:
        :return:
        """
        @wraps(func)
        def execute(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ValueError:
                return False

        return execute

    def __get__(self, instance, owner=None) -> Any:
        return self._value

    def __set__(self, instance, value: Any) -> NoReturn:
        if self.is_constant and self.__post_init:
            raise NotImplementedError("Constants can not be assigned in runtime")

        if not self.validate(value):
            raise ValueError(f"Invalid value to be set for property {self}")

        self._value = value
        self.loader[self.key] = self.dump_caster()

    def __repr__(self):
        return f"{self.key} in {self.loader} = {self._value}"


__all__ = ["AbstractConfigVar"]
