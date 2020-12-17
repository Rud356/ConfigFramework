from ConfigFramework.custom_types import *

__version__ = "1.3.1"


class BaseConfig:
    """
    BaseConfig class that adds some functions to be able to use them with whole thing together.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        pass

    def dump(self) -> None:
        """
        Dumps all variables in config to their providers.

        :return:
        """
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
