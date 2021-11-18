from collections import ChainMap
from typing import Optional, MutableMapping, Any, Tuple

from config_framework.types.abstract import AbstractLoader
from config_framework.types.variable_key import VariableKey


class Composite(AbstractLoader):
    loaders: Tuple[AbstractLoader, ...]

    def __init__(
        self, data: MutableMapping[str, Any],
        defaults: MutableMapping[str, Any],
        loaders: Tuple[AbstractLoader, ...]
    ):
        super().__init__(data, defaults)
        self.loaders = loaders

    @classmethod
    def load(
        cls, *loaders,
        defaults: Optional[MutableMapping[str, Any]] = None
    ):
        return cls(
            data=ChainMap(*loaders),
            defaults=defaults or {},
            loaders=loaders
        )

    def dump(self, include_defaults: bool = False) -> None:
        for loader in self.loaders:
            loader.dump()

    def __delitem__(self, key: VariableKey) -> None:
        error_counter = 0
        for loader in self.loaders:
            try:
                del loader[key]

            except KeyError:
                error_counter += 1

        if error_counter == len(self.loaders):
            raise KeyError(
                f"Couldn't find any value using key: {key}"
            )
