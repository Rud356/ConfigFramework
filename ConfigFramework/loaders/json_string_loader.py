import json
from collections import ChainMap, Mapping
from typing import AnyStr, Dict, Union

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class JsonStringLoader(AbstractConfigLoader):
    def __init__(self, data: Union[Dict, ChainMap, Mapping], defaults: Dict):
        super().__init__(data, defaults)

    @classmethod
    def load(cls, config: AnyStr, defaults: Dict = None):
        data = json.loads(config)

        return cls(data, defaults)

    def dump(self, include_defaults: bool = False, **json_kwargs) -> AnyStr:
        to_dump = self.data

        if include_defaults:
            to_dump = dict(self.lookup_data)

        return json.dumps(to_dump, ensure_ascii=False, check_circular=True, **json_kwargs)
