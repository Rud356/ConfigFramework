from typing import Optional, MutableMapping, Any

from config_framework.types.abstract import AbstractLoader


class Dict(AbstractLoader):
    @classmethod
    def load(
        cls, data: MutableMapping[str, Any],
        defaults: Optional[MutableMapping[str, Any]] = None
    ):
        return cls(data=data, defaults=defaults or {})

    def dump(self, include_defaults: bool = False) -> None:
        """
        This method doesn't changes anything since dict is updated whenever
        values are changed.

        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.
        """
        pass
