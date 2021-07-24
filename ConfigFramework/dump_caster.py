from __future__ import annotations

from typing import Any, Callable, Dict, TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
    from ConfigFramework.abstract.abc_variable import AbstractConfigVar


class DumpCaster:
    """
    Class that is meant to help assigning specific dump caster function for different ConfigLoaders.

    Saved for backward compatibility. Recommended to use AbstractConfigVar as typehint.
    """
    def __init__(self, casters_dict: Dict[
            Union[Type[AbstractConfigLoader], str],
            Callable[[AbstractConfigVar], Any]
    ]):
        """
        Creates a caster for some variable, that can execute functions depending on what caster type it received.
        If you want to set default caster - set '*' key to casters_mapping

        :param casters_dict: a dictionary with AbstractConfigLoader or '*' as key and callable, that returns something
         as config_var.
         '*' key represents default caster for any unlisted caster.

        """
        self.casters_mapping: Dict[
            Union[Type[AbstractConfigLoader], str],
            Callable[[AbstractConfigVar], Any]
        ] = casters_dict

    def __call__(self, config_var: AbstractConfigVar) -> Any:
        caster_default: Callable[[AbstractConfigVar], Any] = self.casters_mapping.get('*', lambda v: v)
        loader_type = config_var._loader_type() # noqa: _loader_type should be just internal function
        return self.casters_mapping.get(loader_type, caster_default)(config_var.value)

    def __repr__(self):
        return str(self.casters_mapping)
