from typing import Any, AnyStr, Callable, Hashable, Optional, Tuple

from ConfigFramework import DumpCaster, loaders, variables
from ConfigFramework.abstract import AbstractConfigLoader, AbstractConfigVar

# This is example of how you can get to some value underneath of other dictionaries, that been loaded from config
variable = variables.ConfigVar("some/path/to/nested/value", ...)


def caster(value):
    # Here you can do whatever you wish with your variable and return required type that will be used in code
    return str(value)


def dump_caster(config_var: variables.ConfigVar):
    # Here you can do whatever you need to save this variable in a way it will be easier to load for you
    return int(config_var.value)


# This will help you with choosing correct way to cast variable, depending on where it was loaded from
advanced_dump_caster = DumpCaster({
    loaders.JsonLoader: dump_caster,  # Setting dump function for specific loader
    '*': str  # Default dump_caster function for loaders that aren't listed here
})

casted_variable = variables.ConfigVar("variable", ..., caster=caster, dump_caster=advanced_dump_caster)

# Variables can be created as constants or made constant afterwards
variable_constant = variables.ConfigVar("some/path/to/nested/value", ..., constant=True)
variable_decorated_constant = variables.constant_var(variables.ConfigVar("some/path/to/nested/value", ...))


# Variables can be also defined by inheriting the ConfigFramework.abstract.AbstractConfigVar
# Here's example of BoolVar inside of ConfigFramework.variables
class BoolVar(AbstractConfigVar):
    def __init__(
        self, key: [Hashable, AnyStr], loader: AbstractConfigLoader, *,
        dump_caster: Optional[Callable, DumpCaster] = None, validator: Optional[Callable] = None,
        default: Optional[Any] = None, true_str_values: Tuple[AnyStr] = ("true", "t", "y", "1"), constant: bool = False
    ):
        super().__init__(
            key, loader, typehint=bool, dump_caster=dump_caster,
            validator=validator, default=default, constant=constant
        )
        self._true_str_values: set = set(true_str_values)

    # Also you can define casters/dump_casters/validators right inside of your class
    def caster(self, value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in self._true_str_values

        if isinstance(value, (bool, int, float)):
            return value > 0

        return False
