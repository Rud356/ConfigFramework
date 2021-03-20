# Here we'll take a look onto how we exactly create our custom loader
# As example we'll take realisation of JsonStringLoader

import json
from collections import ChainMap, Mapping
from functools import partial
from typing import AnyStr, Dict, Optional, Union

from ConfigFramework.abstract import AbstractConfigLoader


class JsonStringLoader(AbstractConfigLoader):
    # This is a place where I put loaders and dumpers to make it easier to switch in case you need to
    json_serialized_loader = json.loads
    json_serialized_dumper = partial(json.dumps, ensure_ascii=False, check_circular=True, indent=2)

    def __init__(self, data: Union[Dict, ChainMap, Mapping], defaults: Dict):
        # This stage must always exist in any of loaders
        # because it handles the data and defaults placing, which are required to work properly with everything else
        super().__init__(data, defaults)

    @classmethod
    def load(cls, config: AnyStr, defaults: Optional[Dict] = None, **json_kwargs):
        # Here we define our data loading that will result a dictionary or some mapping that we'll pass to __init__
        data = cls.json_serialized_loader(config, **json_kwargs)

        return cls(data, defaults)

    def dump(self, include_defaults: bool = False, **json_kwargs) -> AnyStr:
        # Here we define how we gonna dump our data into loader, if there's a way to
        to_dump = self.data

        # This is how you can also include defaults into your dump
        # Since include_defaults is important argument - I think it worth adding this line, before dumping values
        if include_defaults:
            # Default values and loaded data is placed all together in self.lookup_data, which is collections.ChainedMap
            # instance, which we cast to dict before dumping
            to_dump = dict(self.lookup_data)

        return self.__class__.json_serialized_dumper(to_dump, ensure_ascii=False, check_circular=True, **json_kwargs)
