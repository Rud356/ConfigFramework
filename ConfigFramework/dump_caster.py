from __future__ import annotations
from typing import AnyStr, Callable, Dict, TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
    from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class DumpCaster:
    """
    Class that is meant to help assigning specific dump caster function for different ConfigLoaders.
    """
    def __init__(self, casters_dict: Dict[Union[AbstractConfigLoader, AnyStr], Callable]):
        """
        Creates a caster for some variable, that can execute functions depending on what caster type it received.
        If you want to set default caster - set '*' key to casters_mapping

        :param casters_dict: a dictionary with AbstractConfigLoader or '*' as key and callable, that returns something
         as value.
         '*' key represents default caster for any unlisted caster.
        """
        self.casters_mapping = casters_dict

    def __call__(self, value: AbstractConfigVar):
        default: Callable = lambda v: v
        if '*' in self.casters_mapping.keys():
            default: Callable = self.casters_mapping['*']

        return self.casters_mapping.get(value.loader, default)(value)
