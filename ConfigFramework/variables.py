from typing import Any, AnyStr, Callable, Hashable, NoReturn, Optional, TYPE_CHECKING, Type

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class ConfigVar(AbstractConfigVar):
    # Yes, its literally the same thing
    pass


class IntVar(AbstractConfigVar):
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
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable] = None, validator: Optional[Callable] = None, default: Optional[Any] = None
    ):
        super().__init__(
            key, loader, typehint=bool, dump_caster=dump_caster,
            validator=validator, default=default
        )

    def caster(self, value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in {"true", "t", "y", "1"}

        if isinstance(value, (bool, int, float)):
            return value > 0

        return False

    def __get__(self, instance, owner=None) -> bool:
        return super(BoolVar, self).__get__(instance)

    def __set__(self, instance, value: bool) -> NoReturn:
        super(BoolVar, self).__set__(instance, value)
