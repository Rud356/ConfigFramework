from os import environ
from typing import Optional, MutableMapping, Any

from config_framework.types.abstract import AbstractLoader


class Environment(AbstractLoader):
    @classmethod
    def load(cls, defaults: Optional[MutableMapping[str, Any]] = None):
        """
        Loads data from environment.

        :param defaults: default values.
        :return: instance of env loader.
        """
        return cls(data=dict(environ), defaults=defaults or {})

    def dump(self, include_defaults: bool = False) -> None:
        """
        This method doesn't change env variables at all
        because not many types, convert properly into string env variable
        and can be loaded back.

        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.
        """
        pass
