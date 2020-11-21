from ConfigFramework.custom_types import *


class BaseConfig:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        pass

    def dump(self):
        _loaders = set()

        for key in dir(self):
            var = getattr(self, key)

            if isinstance(var, ConfigVariable):
                _loaders.add(var.loader)

        for loader in _loaders:
            loader.dump()

    def __repr__(self):
        return "\n".join(
            filter(lambda var: isinstance(var, ConfigVariable), [var for var in dir(self)])
        )

    def __str__(self):
        return repr(self)

