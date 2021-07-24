from __future__ import annotations

from typing import Any, Callable, Optional, Tuple, Type, Union

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar, Var
from ConfigFramework.custom_types import key_type


class ConfigVar(AbstractConfigVar):
    # Yes, its literally the same thing
    """
    Represents any config variable that you can customize to your needs by adding some code.
    """

    def __init__(
        self, key: key_type,
        loader: AbstractConfigLoader, *,
        typehint: Optional[Union[Type, Any]] = Any,
        caster: Optional[Callable[[Any], Var]] = None,
        dump_caster: Optional[Callable[[AbstractConfigVar], Any]] = None,
        validator: Optional[Callable[[Var], bool]] = None,
        default: Optional[Any] = None,
        constant: bool = False
    ):
        """
        Initializes variable for specified first_loader and key.

        :param key: Any hashable, string or Path instance. Example
            of how to get such vars: `config_root/database/database_ip`. Warning:
            you must not start config paths with / or \\ since it may cause unwanted errors
            because `pathlib.Path` is used to transform these to keys sequence.
        :param loader: A first_loader that will be looked up to get vars config_var or to update values.
        :param typehint: Typehint for __value field, that by default being returned.
        :param caster: Callable that should return variable casted to specific type (in case you need custom types).
        :param dump_caster: Callable that being called when config being dumped. Also can be instance of
         ConfigFramework.dump_caster.DumpCaster.
        :param validator: Callable that validates config_var or defaults in case the original config_var is invalid.
        :param default: Default config_var that will be set, if config_var is invalid.
        :param constant: Sets if variable config_var can be set in runtime.

        .. versionadded:: 2.1.0
           pathlib.Path support as variable key.

        .. versionadded:: 2.2.0
            ConfigVar can be used as a type hint.

        .. deprecated:: 2.2.0
            typehint parameter is deprecated and will be deleted in 2.5.0. To use type hints use
            ConfigVar[desired_type] instead.
        """

        super().__init__(
            key, loader, typehint=typehint, caster=caster,
            dump_caster=dump_caster, validator=validator, default=default, constant=constant
        )


class IntVar(AbstractConfigVar):
    """
    Represents an integer config_var in your config.

    """
    value: int

    def __init__(
        self, key: key_type, loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable[[AbstractConfigVar], Any]] = None,
        validator: Optional[Callable[[int], bool]] = None,
        default: Optional[Any] = None,
        constant: bool = False
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
    value: float

    def __init__(
        self, key: key_type,
        loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable[[AbstractConfigVar], Any]] = None,
        validator: Optional[Callable[[float], bool]] = None,
        default: Optional[Any] = None,
        constant: bool = False
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
    value: bool

    def __init__(
        self, key: key_type,
        loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable[[AbstractConfigVar], Any]] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        default: Optional[Any] = None,
        true_str_values: Tuple[str, ...] = ("true", "t", "y", "1"),
        constant: bool = False
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
