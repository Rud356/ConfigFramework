from typing import Any, AnyStr, Callable, Hashable, List, NoReturn, Optional

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class ConfigVar(AbstractConfigVar):
    # Yes, its literally the same thing
    """
    Represents any config variable that you can customize to your needs by adding some code.

    """
    pass


class IntVar(AbstractConfigVar):
    """
    Represents an integer value in your config.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable] = None, validator: Optional[Callable] = None, default: Optional[Any] = None
    ):
        super().__init__(
            key, loader, caster=int, typehint=int, dump_caster=dump_caster,
            validator=validator, default=default
        )

    def __get__(self, instance, owner=None) -> int:
        return super(IntVar, self).__get__(instance)

    def __set__(self, instance, value: int) -> NoReturn:
        super(IntVar, self).__set__(instance, value)


class FloatVar(AbstractConfigVar):
    """
    Represents an float value in your config.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable] = None, validator: Optional[Callable] = None, default: Optional[Any] = None
    ):
        super().__init__(
            key, loader, caster=float, typehint=float, dump_caster=dump_caster,
            validator=validator, default=default
        )

    def __get__(self, instance, owner=None) -> float:
        return super(FloatVar, self).__get__(instance)

    def __set__(self, instance, value: float) -> NoReturn:
        super(FloatVar, self).__set__(instance, value)


class BoolVar(AbstractConfigVar):
    """
    Represents boolean variables in your config with customizable set of words that considered as correct.

    """
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable] = None, validator: Optional[Callable] = None, default: Optional[Any] = None,
        true_str_values: List[AnyStr] = ("true", "t", "y", "1")
    ):
        super().__init__(
            key, loader, typehint=bool, dump_caster=dump_caster,
            validator=validator, default=default
        )
        self._true_str_values = set(true_str_values)

    def caster(self, value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in self._true_str_values

        if isinstance(value, (bool, int, float)):
            return value > 0

        return False

    def __get__(self, instance, owner=None) -> bool:
        return super(BoolVar, self).__get__(instance)

    def __set__(self, instance, value: bool) -> NoReturn:
        super(BoolVar, self).__set__(instance, value)


def constant_var(config_var: AbstractConfigVar) -> AbstractConfigVar:
    """
    Makes variable unable to be assigned on runtime.

    :param config_var: variable that already been initialized.
    :return:
    """

    def not_implemented_assigning(*args, **kwargs):
        raise NotImplementedError("Constants can not be assigned in runtime")

    config_var.is_constant = True
    config_var.__set__ = not_implemented_assigning
    return config_var

