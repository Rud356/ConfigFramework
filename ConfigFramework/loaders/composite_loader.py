from collections import ChainMap
from typing import Dict, NoReturn, Optional

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class CompositeLoader(AbstractConfigLoader):
    def __init__(self, *loaders: AbstractConfigLoader, defaults: Dict):
        super().__init__(ChainMap(*loaders), defaults=defaults)
        self.loaders = loaders

    def dump(self, include_defaults: bool = False) -> NoReturn:
        for loader in self.loaders:
            loader.dump()

    def dump_to(self, other_loader: AbstractConfigLoader, include_defaults: bool = False) -> NoReturn:
        data = dict(ChainMap(*[loader.data for loader in self.loaders]))
        defaults = {}

        if include_defaults:
            defaults = dict(ChainMap(*[loader.defaults for loader in self.loaders]))

        other_loader.data = data
        other_loader.defaults = defaults
        other_loader.dump(include_defaults=include_defaults)

    def __setitem__(self, key, value):
        """
        Sets variable config_var inside of your loaders that are hidden underneath composite first_loader.

        :param key: a key that points at what variable you want to set config_var to.
        :param value: a new config_var for variable.
        :return: nothing.
        """

        for loader in self.loaders:
            try:
                loader[key] = value
                loader.dump()

            except KeyError:
                continue

            else:
                break

    @classmethod
    def load(cls, *loaders: AbstractConfigLoader, defaults: Optional[Dict] = None):
        return cls(*loaders, defaults=defaults)
