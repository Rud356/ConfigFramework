import typing
from pathlib import Path
from typing import AnyStr, Callable, Hashable, Union

from ConfigFramework import abstract

T = typing.TypeVar('T')


class VariableType(typing.Generic[T]):
    """Variable typehint that helps you with telling apart what's inside of variable."""
    key: Union[Hashable, AnyStr, Path]
    value: T
    is_constant: bool
    loader: abstract.AbstractConfigLoader

    caster: Callable
    dump_caster: Callable
    validate: Callable
