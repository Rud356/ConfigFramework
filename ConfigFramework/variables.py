from __future__ import annotations

from typing import Any, AnyStr, Callable, Hashable, Optional, Tuple, Type

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar
from .dump_caster import DumpCaster


class ConfigVar(AbstractConfigVar):
    # Yes, its literally the same thing
    """
    Represents any config variable that you can customize to your needs by adding some code.

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
        super().__init__(
            key, loader, typehint=typehint, caster=caster,
            dump_caster=dump_caster, validator=validator, default=default, constant=constant
        )


class IntVar(AbstractConfigVar):
    """
    Represents an integer config_var in your config.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable, DumpCaster] = None, validator: Optional[Callable] = None,
        default: Optional[Any] = None, constant: bool = False
    ):
        """
        Initializes int variable for specified first_loader and key.

        :param key: Any hashable or a string. Strings can be written as paths in case you need a variable.
         that underlies other mappings. Example of how to get such vars: `config_root/database/database_ip`.
        :param loader: A first_loader that will be looked up to get vars config_var or to update values.
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster
        :param validator: Callable that validates config_var or defaults in case the original config_var is invalid.
        :param default: Default config_var that will be set, if config_var is invalid.
        """
        super().__init__(
            key, loader, caster=int, typehint=int, dump_caster=dump_caster,
            validator=validator, default=default, constant=constant
        )


class FloatVar(AbstractConfigVar):
    """
    Represents an float config_var in your config.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable, DumpCaster] = None, validator: Optional[Callable] = None,
        default: Optional[Any] = None, constant: bool = False
    ):
        """
        Initializes float variable for specified first_loader and key.

        :param key: Any hashable or a string. Strings can be written as paths in case you need a variable.
         that underlies other mappings. Example of how to get such vars: `config_root/database/database_ip`.
        :param loader: A first_loader that will be looked up to get vars config_var or to update values.
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster
        :param validator: Callable that validates config_var or defaults in case the original config_var is invalid.
        :param default: Default config_var that will be set, if config_var is invalid.
        :param constant: Sets if variable config_var can be set in runtime
        """

        super().__init__(
            key, loader, caster=float, typehint=float, dump_caster=dump_caster,
            validator=validator, default=default, constant=constant
        )


class BoolVar(AbstractConfigVar):
    """
    Represents boolean variables in your config with customizable set of words that considered as correct.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable, DumpCaster] = None, validator: Optional[Callable] = None,
        default: Optional[Any] = None, true_str_values: Tuple[AnyStr] = ("true", "t", "y", "1"), constant: bool = False
    ):
        """
        Initializes variable for specified first_loader and key.

        :param key: Any hashable or a string. Strings can be written as paths in case you need a variable.
         that underlies other mappings. Example of how to get such vars: `config_root/database/database_ip`.
        :param loader: A first_loader that will be looked up to get vars config_var or to update values.
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster
        :param validator: Callable that validates config_var or defaults in case the original config_var is invalid.
        :param default: Default config_var that will be set, if config_var is invalid.
        """
        self._true_str_values: set = set(true_str_values)
        super().__init__(
            key, loader, typehint=bool, dump_caster=dump_caster,
            validator=validator, default=default, constant=constant
        )

    def caster(self, value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in self._true_str_values

        if isinstance(value, (bool, int, float)):
            return value > 0

        return False


def constant_var(config_var: AbstractConfigVar) -> AbstractConfigVar:
    """
    Makes variable unable to be assigned on runtime.

    :param config_var: variable instance.
    :return: same ConfigVar instance, but its value can't be reassigned on a runtime.
    """
    config_var.is_constant = True
    return config_var
