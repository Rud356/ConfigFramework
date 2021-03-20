import json
from collections import ChainMap, Mapping
from functools import partial
from typing import AnyStr, Dict, Optional, Union

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class JsonStringLoader(AbstractConfigLoader):
    json_serialized_loader = json.loads
    json_serialized_dumper = partial(json.dump, ensure_ascii=False, check_circular=True, indent=2)

    def __init__(self, data: Union[Dict, ChainMap, Mapping], defaults: Dict):
        super().__init__(data, defaults)

    @classmethod
    def load(cls, config: AnyStr, defaults: Optional[Dict] = None, **json_kwargs):
        data = cls.json_serialized_loader(config, **json_kwargs)

        return cls(data, defaults)

    def dump(self, include_defaults: bool = False, **json_kwargs) -> AnyStr:
        to_dump = self.data

        if include_defaults:
            to_dump = dict(self.lookup_data)

        return self.__class__.json_serialized_dumper(to_dump, ensure_ascii=False, check_circular=True, **json_kwargs)
