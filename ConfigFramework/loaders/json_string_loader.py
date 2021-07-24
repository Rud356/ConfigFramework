import json
from functools import partial
from typing import AnyStr

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader
from ConfigFramework.custom_types import data_type, defaults_type


class JsonStringLoader(AbstractConfigLoader):
    json_serialized_loader = json.loads
    json_serialized_dumper = partial(json.dumps, ensure_ascii=False, check_circular=True, indent=2)

    def __init__(self, data: data_type, defaults: defaults_type):
        super().__init__(data, defaults)

    @classmethod
    def load(cls, config: AnyStr, defaults: defaults_type = None, **json_kwargs):  # type: ignore
        data = cls.json_serialized_loader(config, **json_kwargs)

        return cls(data, defaults)

    def dump(self, include_defaults: bool = False, **json_kwargs) -> str:  # type: ignore
        to_dump = self.data

        if include_defaults:
            to_dump = dict(self.lookup_data)

        return self.__class__.json_serialized_dumper(
            to_dump, ensure_ascii=False,
            check_circular=True, **json_kwargs
        )
