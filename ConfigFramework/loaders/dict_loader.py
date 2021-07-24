from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.custom_types import data_type, defaults_type


class DictLoader(AbstractConfigLoader):
    """Uses dictionaries with same interface as if it was an Loader."""
    @classmethod
    def load(cls, data: data_type, defaults: defaults_type = None):  # type: ignore
        """
        Loads dictionary as some loader with same interface.

        :param data: your dictionary with settings.
        :param defaults: default values.
        :return: instance of DictLoader.
        """
        return cls(data, defaults=defaults)

    def dump(self, include_defaults: bool = False) -> None:
        """
        No need to dump at all since all values instantly being updated.
        Left only for compatibility purpose.

        :param include_defaults: doesn't affect anything as stated before.
        :return: nothing.
        """
        pass
