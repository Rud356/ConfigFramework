from __future__ import annotations

import typing
import warnings
from collections import ChainMap
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Callable, Dict, Hashable, Optional, Union

if typing.TYPE_CHECKING:
    from .dump_caster import DumpCaster
    from .abstract import AbstractConfigLoader, AbstractConfigVar

key_type = Union[Hashable, str, Path]
data_type = Union[
    ChainMap,
    MutableMapping,
    Dict[Hashable, Any]
]
defaults_type = Optional[Dict[key_type, Any]]
Var = typing.TypeVar('Var')


class VariableType(typing.Generic[Var]):
    """
    Variable typehint that helps you with telling apart what's inside of variable.

    .. deprecated:: 2.2.0
        VariableType type hint is deprecated and will be deleted in 2.5.0. To use type hints use ConfigVar
        instead.

    """
    warnings.warn(
        "VariableType class will be deleted in version 2.5.0, please "
        "consider using use of ConfigVar or any other classes as typehint instead of this one",
        DeprecationWarning
    )

    key: key_type
    value: Var
    is_constant: bool
    loader: AbstractConfigLoader

    caster: Optional[Callable[[Any], Var]]
    dump_caster: Optional[
        Union[Callable[[AbstractConfigVar], Any], DumpCaster]
    ]
    validate: Optional[Callable[[Var], bool]]
