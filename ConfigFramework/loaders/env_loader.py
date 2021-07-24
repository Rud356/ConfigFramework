from os import environ
from typing import NoReturn

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.custom_types import defaults_type


class EnvLoader(AbstractConfigLoader):
    @classmethod
    def load(cls, defaults: defaults_type = None):  # type: ignore
        # Environ is actually a MutableMapping so this error is mypy mistake
        return cls(data=environ, defaults=defaults)  # type: ignore

    def dump(self, include_defaults: bool = False) -> NoReturn:
        """
        You can not dump values to environ yet because I don't know a good way to do that or think it's needed.
        Left only for compatibility purpose.

        :param include_defaults: doesn't affect anything as stated before.
        :return: nothing.
        """
        ...
