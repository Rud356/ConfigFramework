import json
from collections import ChainMap, Mapping
from os import PathLike
from pathlib import Path
from typing import AnyStr, Dict, NoReturn, Union

from ConfigFramework.abstract.abc_loader import AbstractConfigLoader


class JsonLoader(AbstractConfigLoader):
    def __init__(self, data: Union[Dict, ChainMap, Mapping], defaults: Dict, config_path: Path):
        super().__init__(data, defaults)
        self.config_path = config_path

    @classmethod
    def load(cls, config_path: Union[AnyStr, Path, PathLike], defaults: Dict):
        config_path = Path(config_path)

        if not config_path.is_file():
            raise ValueError(f"Invalid file path: {config_path}")

        with open(config_path, encoding="utf8") as json_f:
            data = json.load(json_f)

        return cls(data, defaults, config_path=config_path)

    def dump(self, include_defaults: bool = False, **json_kwargs) -> NoReturn:
        to_dump = self.data

        if include_defaults:
            to_dump = dict(self.lookup_data)

        with open(self.config_path, 'w', encoding="utf8") as json_f:
            json.dump(to_dump, json_f, ensure_ascii=False, check_circular=False, **json_kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.config_path}"
