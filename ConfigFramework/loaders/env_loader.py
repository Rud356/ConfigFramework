from os import environ
from typing import Dict, NoReturn, Optional

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class EnvLoader(AbstractConfigLoader):
    @classmethod
    def load(cls, defaults: Optional[Dict] = None):
        return cls(data=environ, defaults=defaults)

    def dump(self, include_defaults: bool = False) -> NoReturn:
        """
        You can not dump values to environ yet because I don't know a good way to do that or think it's needed.
        Left only for compatibility purpose.

        :param include_defaults: doesn't affect anything as stated before.
        :return: nothing.
        """
        pass
