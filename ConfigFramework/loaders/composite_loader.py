from collections import ChainMap
from typing import Dict, NoReturn

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class CompositeLoader(AbstractConfigLoader):
    def __init__(self, *loaders: AbstractConfigLoader, defaults: Dict):
        super().__init__(ChainMap(*loaders), defaults)
        self.loaders = loaders

    def dump(self, include_defaults: bool = False) -> NoReturn:
        for loader in self.loaders:
            loader.dump()

    def dump_to(self, other_loader: 'AbstractConfigLoader', include_defaults: bool = False) -> NoReturn:
        data = dict(ChainMap(*[loader.data for loader in self.loaders]))
        defaults = {}

        if include_defaults:
            defaults = dict(ChainMap(*[loader.defaults for loader in self.loaders]))

        other_loader.data = data
        other_loader.defaults = defaults
        other_loader.dump(include_defaults=include_defaults)

    @classmethod
    def load(cls, *loaders: AbstractConfigLoader, defaults: Dict):
        return cls(*loaders, defaults=defaults)
