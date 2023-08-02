from typing import Optional, MutableMapping, Any

from config_framework.types.abstract import AbstractLoader


class Dict(AbstractLoader):
    @classmethod
    def load(
        cls, data: MutableMapping[str, Any],
        defaults: Optional[MutableMapping[str, Any]] = None
    ):
        """
        Wrapper for dicts usage as config source.

        :param data: argument expects dictionary that will be used as source.
        :param defaults: default values.
        :return: instance of dict loader.
        """
        return cls(data=data, defaults=defaults or {})

    def dump(self, include_defaults: bool = False) -> None:
        """
        This method doesn't change anything since dict is updated whenever
        values are changed.

        :param include_defaults: specifies if
            you want to have default variables to be dumped.
        :return: nothing.
        """
        pass
